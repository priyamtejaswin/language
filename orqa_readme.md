Commands
===

```bash
# GPU training
export CUDA_VISIBLE_DEVICES=0
export TF_FORCE_GPU_ALLOW_GROWTH=true
export MODEL_DIR=./model_dir
TF_CONFIG='{"cluster": {"chief": ["host:port"]}, "task": {"type": "chief", "index": 0}}' \
python -m language.orqa.experiments.orqa_experiment \
  --retriever_module_path=./ict \
  --block_records_path=./enwiki-20181220/blocks.tfr \
  --data_root=./qresplit \
  --model_dir=$MODEL_DIR \
  --dataset_name=NaturalQuestions \
  --num_train_steps=$(( 3417 * 20 )) \
  --save_checkpoints_steps=1000
```


```bash
# Final test evaluation
export MODEL_DIR=./model_dir
python -m language.orqa.predict.orqa_eval \
  --dataset_path=./qresplit/NaturalQuestions.resplit.test.jsonl \
  --model_dir=$MODEL_DIR
```
