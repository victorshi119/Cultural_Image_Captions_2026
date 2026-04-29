import json
import itertools
import os

learning_rates = [1e-4, 5e-5, 1e-5, 6.5e-4]
warmup_steps_list = [0.01, 0.1]
schedule = ["cosine", "linear", "inverse_sqrt"]
epochs = [8, 16, 24]
batch_size = [16, 32]

combinations = itertools.product(learning_rates, warmup_steps_list, schedule, epochs, batch_size)

for idx, (lr, warmup_steps, schedule, epochs, batch_size) in enumerate(combinations):
    config = {
        "output_dir" : f"/home/saycock/personal/mtob/scripts/configs/array/nllb-1B-kgv-eng-lr{lr}-warm{warmup_steps}-sched{schedule}-{epochs}ep-b{batch_size}",
        "warmup_ratio": warmup_steps,
        "learning_rate": lr,
        "lr_scheduler_type": schedule,
         "num_train_epochs": epochs,
        "per_device_train_batch_size": batch_size,

        "model_name_or_path": "facebook/nllb-200-distilled-1.3B",
        "train_file": "/home/saycock/personal/mtob/splits/eng-kgv-train.json",
        "validation_file": "/home/saycock/personal/mtob/splits/eng-kgv-dev-500.json",
        "test_file": "/home/saycock/personal/mtob/splits/eng-kgv-test.json",
        "source_lang": "kgv_Latn",
        "target_lang": "eng_Latn",

        "max_source_length": 128,
        "max_target_length": 128,
        "per_device_eval_batch_size": 8,
        "num_beams": 10,
        "seed": 42,

        "do_train": "True",
        "do_eval": "True",
        "do_predict":"True",
        "predict_with_generate": "True",
        "overwrite_output_dir": "True",

        "forced_bos_token": "eng_Latn",
        "evaluation_strategy": "epoch",
        "save_strategy": "epoch",
        "metric_for_best_model": "chrf",
        "greater_is_better": "True",
        "optim": "adamw_torch",
        "load_best_model_at_end": "True",
        "save_total_limit": 1

    }
    
    config_file = os.path.join('configs/array', f'config_{idx}.json')
    
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=4)
