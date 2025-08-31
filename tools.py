import json
from typing import List, Dict

from pydantic import BaseModel
from pydantic_ai import BinaryContent
#from tifffile import imagej_description
from torch.fx.experimental.unification import unify
#from schemas import BreakFastBoxModel, ObjectRuleModel
from schemas import  ObjectRuleModel
from agent import AnomalyDetectionAgent
from prompts import checklist_prompt
from schemas import CheckListModel, AnalysisResponse
from prompts import system_prompt
import asyncio
import time
from utils import read_bytes_image, resize_image


async def run_batches(args, batches: List[Dict], concurrency_limit=10):
    sem = asyncio.Semaphore(concurrency_limit)

    async def task(batch):
        async with sem:
            try:
                t1 = time.time()
                query_image = resize_image(read_bytes_image(batch['image_path']))
                #query_image = read_bytes_image(batch['image_path'])
                schema_map = batch['schema_map']
                object_name = batch['object_name']
                unified_rule = batch['unified_rule']
                agent = AnomalyDetectionAgent(args)
                history = agent.build_history(system_prompt)

                text_prompt = "Create a detailed description for each object in the image, including the container or package if applicable."
                user_prompt = [text_prompt, query_image]

                results = await agent.run(user_prompt=user_prompt, message_history=history, output_type=List[schema_map[object_name]])
                image_description = [obj.model_dump(exclude_none=True) for obj in results.output]
                print(batch['image_path'], image_description)
                usage_1 = agent.usage
                rule_text = str(unified_rule)
                rule_text += f"""\nTest image description: \n{image_description}\n
                                                 Does the test image description have an anomaly regarding the object rules?
                                                 All objects in the rule are required in the test image description. 
                                                 All objects in the test image description are required in the object rules.
                                             """
                prompt = [rule_text]
                agent = AnomalyDetectionAgent(args)
                results = await agent.run(user_prompt=prompt, message_history=history, output_type=AnalysisResponse)
                t2 = time.time()
                #time.sleep(2)
                usage_2 = agent.usage
                return {
                    'image_path': batch['image_path'],
                    'object': batch['object_name'],
                    'division': batch['division'],
                    'image': batch['image_name'] ,
                    'elapsed_time': t2 - t1,
                    'has_anomaly': results.output.has_anomaly,
                    'description': results.output.description,
                    'usages': [usage_1, usage_2]
                }
            except Exception as err:
                print("[run_batches] Error processing batch:", batch['image_path'], err)
                raise(err)
                #return {}

    results = await asyncio.gather(*(task(batch) for batch in batches))

    return results

async def run_batch(args, prompts, output_model, concurrency_limit=2):
    sem = asyncio.Semaphore(concurrency_limit)

    async def task(prompt):
        async with sem:
            # return  await agent.run(user_prompt=prompt, output_type=output_model)
            agent = AnomalyDetectionAgent(args)
            history = agent.build_history(system_prompt)
            return await agent.run(user_prompt=prompt, message_history=history, output_type=output_model)

    results = await asyncio.gather(*(task(prompt) for prompt in prompts))

    return results


# async def get_checklist_from_objects(
#         agent: AnomalyDetectionAgent,
#         few_shot_images: Dict[str, List[BinaryContent]],
#         object_name: str
# ):
#     history = agent.build_history(system_prompt)
#     user_prompt = [checklist_prompt, *few_shot_images[object_name]]
#     results = await agent.run(user_prompt=user_prompt, message_history=history, output_type=CheckListModel)
#     return results.all_messages(), results.output.model_dump()['anomalies_checklist']


async def get_complete_description_from_images(
        args,
        few_shot_images: List[BinaryContent],
        output_model: BaseModel
):
    image_descriptions = []
    text_prompt = "Create a detailed description for each object in the image, including the container or package if applicable."
    prompts = []

    # prepare prompts
    for img in few_shot_images:
        user_prompt = [text_prompt, img]
        prompts.append(user_prompt)

    results = await run_batch(args, prompts, List[output_model])
    # print(results)
    #image_descriptions.append([obj.output for obj in results])
    for result in results:
        objs = []
        for obj in result.output:
            objs.append(obj.model_dump())
        image_descriptions.append(objs)
    # print(image_descriptions)
    # results = await agent.run(user_prompt=user_prompt, message_history=history, output_type=List[output_model])
    return image_descriptions


async def get_unfied_rule_from_objects(
        agent: AnomalyDetectionAgent,
        object_models: List[BaseModel],
) -> List[ObjectRuleModel]:
    print("The unifed rule...")
    text_prompt_output = """
        From the description of the objects, create a unified rule for each object.
        Use the following format:
        Object rules:
            Object_name_1 
                property_1: value_1, value_2, ... value_n
                property_2: value_1, value_2, ... value_n

            Object_name_2 
                property_1: value_1, value_2, ... value_n
                property_2: value_1, value_2, ... value_n

            Object_name_3 
                property_1: value_1, value_2, ... value_n
                property_2: value_1, value_2, ... value_n

            Object_name_n 
                property_1: value_1, value_2, ... value_n
                property_2: value_1, value_2, ... value_n
        """
    history = agent.build_history(system_prompt)
    user_prompt = [json.dumps(object_models), text_prompt_output]
    print(user_prompt)
    results = await agent.run(user_prompt=user_prompt, message_history=history, output_type=str)
    return results.output
