import asyncio
import yaml
from box import Box
from itertools import product
from datasets import load_mvtec_loco_anomaly
from agent import AnomalyDetectionAgent
from tools import get_complete_description_from_images, get_unfied_rule_from_objects, run_batches
from billing import calculate_all_costs
from maps import schema_map
from datetime import datetime
from utils import (
    read_bytes_image,
    resize_image
)
from metrics import (
    build_metrics_mapping,
    copmute_binary_metrics,
    save_metrics,
)

async def mvtec_loco_experiment(args: Box):
    # start agent
    anomaly_agent = AnomalyDetectionAgent(args)
    dataset = load_mvtec_loco_anomaly(path=args.dataset.path)
    metrics_mapping = build_metrics_mapping(dataset)

    # prepare few-shot images
    few_shot_images = Box(default_box=True)
    image_descriptions_box = Box(default_box=True)
    train_images_path = args.object['train']
    unifed_rule = ''

    for object_name, image_paths in dataset.train.items():
        if object_name != args.object['name']: continue
        for image_path in image_paths:
            if image_path.name in train_images_path:
                print(image_path.name)
        few_shot_images[object_name] = [resize_image(read_bytes_image(image_path)) for image_path in image_paths if image_path.name in train_images_path]
        image_descriptions_box[object_name] = await  get_complete_description_from_images(args, few_shot_images[object_name], schema_map[object_name] )
        unifed_rule = await get_unfied_rule_from_objects(anomaly_agent, image_descriptions_box[object_name])
        print(unifed_rule)

    for idx, image_descriptions in enumerate(image_descriptions_box[args.object['name']]):
        print("Image desciption", idx)
        print(image_descriptions)
        print("\n")

    # run experiment for each object.
    object_name = args.object['name']

    all_answers = []
    all_checklists = {}
    cost_per_tokens_list = []

    # prepare bateches to run in parallel
    for division, image_paths in  dataset.test[object_name].items():
        if division == 'structural_anomalies': continue #or division == 'good': continue
        batches = []
        print(f"\n[PROVIDER] {args.model.provider} | [MODEL] {args.model.llm} | [OBJECT] {object_name} | [DIVISION] {division}")
        # run experiment for each image
        for idx, image_path in enumerate(image_paths[:]):
            batches.append({
                'image_path': image_path,
                'agent': anomaly_agent,                
                'object_name': object_name,
                'division': division,
                'image_name': image_path.name,
                'schema_map': schema_map,
                'unified_rule': unifed_rule
            })

        results = await run_batches(args, batches)

        # compute metrics
        for result in results:
            if result:
                copmute_binary_metrics(result['object'], result['division'], metrics_mapping, result['has_anomaly'])
                
                # calculate all costs, monetary and environmental
                cost_per_tokens_usage_1 = calculate_all_costs(result['usages'][0], 1, args.model.provider, args.model.litellm)
                cost_per_tokens_usage_2 = calculate_all_costs(result['usages'][1], 1, args.model.provider, args.model.litellm)
                cost_per_tokens = {}
                keys = set(cost_per_tokens_usage_1) | set(cost_per_tokens_usage_2)  # União das chaves

                for key in keys:
                    v1 = cost_per_tokens_usage_1.get(key)
                    v2 = cost_per_tokens_usage_2.get(key)

                    if isinstance(v1, (int, float)) and isinstance(v2, (int, float)):
                        cost_per_tokens[key] = v1 + v2
                    elif isinstance(v1, str) and isinstance(v2, str):
                        cost_per_tokens[key] = f"{v1},{v2}"

                cost_per_tokens_list.append(cost_per_tokens)
                print(f"[{datetime.now().isoformat()}] - Processing: {result['image_path'].name} | Result: {result['has_anomaly']} | Description: {result['description']}")

                del result['image_path']
                del result['usages']
                all_answers.append(result)

    save_metrics(args, object_name, metrics_mapping, all_answers, all_checklists, cost_per_tokens_list)

async def experiment_mvtec_ad(args: Box):
    pass

async def experiments(args: Box):

    if args.dataset.name == 'mvtec_loco_anomaly_detection':
        await mvtec_loco_experiment(args)
    else:
        await experiment_mvtec_ad(args)

async def main():
    with open("config.yaml", "r") as f:
        config = Box(yaml.safe_load(f))

    datasets = config.datasets
    models = config.models
    objects = config.mvtec_loco_objects

    combinations = list(product(datasets, models, objects))
    
    for dataset, model, object in combinations:
        print(dataset, model, object)
        args = Box({
            "dataset": dataset,
            "object": object,
            "model": model
        })
        await experiments(args)

if __name__ == '__main__':
    asyncio.run(main())