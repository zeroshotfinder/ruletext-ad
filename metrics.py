import json
import pandas as pd
from pathlib import Path
from box import Box

def build_metrics_mapping(dataset):
    metrics_mapping = Box(default_box=True)
    for object_name, divisions in dataset.test.items():
        for division, image_paths in divisions.items():
            if division == 'good':
                metrics_mapping[object_name][division] = {'tp': 0, 'fn': 0}
            elif division == 'structural_anomalies':
                metrics_mapping[object_name][division] = {'stn': 0, 'sfp': 0}
            elif division == 'logical_anomalies':
                metrics_mapping[object_name][division] = {'ltn': 0, 'lfp': 0}

    return metrics_mapping

def copmute_binary_metrics(object_name, division, metrics_mapping, has_anomaly):
    match division:
        case 'good':
            if has_anomaly:
                metrics_mapping[object_name][division]['fn'] += 1
            else:
                metrics_mapping[object_name][division]['tp'] += 1
        case  'structural_anomalies':
            if has_anomaly:
                metrics_mapping[object_name][division]['stn'] += 1
            else:
                metrics_mapping[object_name][division]['sfp'] += 1
        case  'logical_anomalies':
            if has_anomaly:
                metrics_mapping[object_name][division]['ltn'] += 1
            else:
                metrics_mapping[object_name][division]['lfp'] += 1

def calculate_metrics(tp, fn, tn, fp) -> dict:
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1_score = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
    accuracy = (tp + tn) / (tp + tn + fp + fn) if (tp + tn + fp + fn) > 0 else 0.0

    return {
        'precision': precision,
        'recall': recall,
        'f1_score': f1_score,
        'accuracy': accuracy
    }

def save_metrics(
    args,
    object_name,
    metrics_mapping,
    all_answers,
    all_checklists,
    cost_per_tokens_list
):
    experiment_path = f"results/{args.model.provider}/{args.model.litellm.replace('/', '-')}/{args.dataset.name}/{object_name}"
    experiment_folder = Path(experiment_path)
    experiment_folder.mkdir(parents=True, exist_ok=True)

    object_metrics = []

    obj = {'object': object_name}
    for divison, metrics in metrics_mapping[object_name].items():
        obj = obj | metrics

    structural_metrics = calculate_metrics(obj['tp'], obj['fn'], obj['stn'], obj['sfp'])
    logical_metrics = calculate_metrics(obj['tp'], obj['fn'], obj['ltn'], obj['lfp'])
    structural_logical_metrics = calculate_metrics(obj['tp'], obj['fn'],  obj['stn'] + obj['ltn'], obj['sfp'] + obj['lfp'])

    structural_metrics = {f"structural_{metric}":value for metric, value in structural_metrics.items()}
    logical_metrics = {f"logical_{metric}":value for metric, value in logical_metrics.items()}
    structural_logical_metrics = {f"structural_logical_{metric}":value for metric, value in structural_logical_metrics.items()}
    object_metrics.append(obj | structural_metrics | logical_metrics | structural_logical_metrics)

    df_metrics = pd.DataFrame(object_metrics)
    df_metrics.to_csv(f"{experiment_folder}/metrics.csv", float_format="%.4f", index=False)

    df_answers = pd.DataFrame(all_answers)
    df_answers.to_csv(f"{experiment_folder}/answers.csv", index=False)
    # print(all_checklists)

    if all_checklists:
        concat_checklists = []
        for object, checklist in all_checklists.items():
            concat_checklists += checklist
        df_checklist = pd.DataFrame(concat_checklists)
        df_checklist.to_csv(f"{experiment_folder}/checklist.csv", index=False)

    df_token_cost = pd.DataFrame(cost_per_tokens_list)
    df_token_cost.to_csv(f"{experiment_folder}/cost.csv", index=False)

    with open(f"{experiment_folder}/total_cost.json", 'w') as f:
        data = {
            'provider': str(df_token_cost.provider.iloc[0]),
            'model': str(df_token_cost.model.iloc[0]).replace('/', '-'),
            'average_elapsed_time': float(df_answers.elapsed_time.mean()),
            'total_input_tokens': int(df_token_cost.input_tokens.sum()),
            'total_output_tokens': int(df_token_cost.output_tokens.sum()),
            'total_tokens': int(df_token_cost.total_tokens.sum()),
            'total_prompt_images': int(df_token_cost.total_prompt_images.sum()),
            'total_energy_kwh': float(df_token_cost.energy_kwh.sum()),
            'co2_kg': float(df_token_cost.co2_kg.sum())
        }
        json.dump(data, f, indent=4)