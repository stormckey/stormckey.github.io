# zsh的的参数传递

今天在调用DDPM模型的时候使用官方给的[:octicons-link-16:命令行代码](https://github.com/openai/guided-diffusion)，竟然报错说参数不存在：
命令是
```
MODEL_FLAGS="--attention_resolutions 32,16,8 --class_cond True --diffusion_steps 1000 --dropout 0.1 --image_size 64 --learn_sigma True --noise_schedule cosine --num_channels 192 --num_head_channels 64 --num_res_blocks 3 --resblock_updown True --use_new_attention_order True --use_fp16 True --use_scale_shift_norm True"
python classifier_sample.py $MODEL_FLAGS --classifier_scale 1.0 --classifier_path models/64x64_classifier.pt --classifier_depth 4 --model_path models/64x64_diffusion.pt $SAMPLE_FLAGS
```
报错为：
```
python classifier_sample.py $MODEL_FLAGS --classifier_scale 1.0 --classifier_path models/64x64_classifier.pt --classifier_depth 4 --model_path models/64x64_diffusion.pt $SAMPLE_FLAGS
usage: classifier_sample.py [-h] [--clip_denoised CLIP_DENOISED] [--num_samples NUM_SAMPLES] [--batch_size BATCH_SIZE]
                            [--use_ddim USE_DDIM] [--model_path MODEL_PATH] [--classifier_path CLASSIFIER_PATH]
                            [--classifier_scale CLASSIFIER_SCALE] [--image_size IMAGE_SIZE]
                            [--num_channels NUM_CHANNELS] [--num_res_blocks NUM_RES_BLOCKS] [--num_heads NUM_HEADS]
                            [--num_heads_upsample NUM_HEADS_UPSAMPLE] [--num_head_channels NUM_HEAD_CHANNELS]
                            [--attention_resolutions ATTENTION_RESOLUTIONS] [--channel_mult CHANNEL_MULT]
                            [--dropout DROPOUT] [--class_cond CLASS_COND] [--use_checkpoint USE_CHECKPOINT]
                            [--use_scale_shift_norm USE_SCALE_SHIFT_NORM] [--resblock_updown RESBLOCK_UPDOWN]
                            [--use_fp16 USE_FP16] [--use_new_attention_order USE_NEW_ATTENTION_ORDER]
                            [--learn_sigma LEARN_SIGMA] [--diffusion_steps DIFFUSION_STEPS]
                            [--noise_schedule NOISE_SCHEDULE] [--timestep_respacing TIMESTEP_RESPACING]
                            [--use_kl USE_KL] [--predict_xstart PREDICT_XSTART]
                            [--rescale_timesteps RESCALE_TIMESTEPS] [--rescale_learned_sigmas RESCALE_LEARNED_SIGMAS]
                            [--classifier_use_fp16 CLASSIFIER_USE_FP16] [--classifier_width CLASSIFIER_WIDTH]
                            [--classifier_depth CLASSIFIER_DEPTH]
                            [--classifier_attention_resolutions CLASSIFIER_ATTENTION_RESOLUTIONS]
                            [--classifier_use_scale_shift_norm CLASSIFIER_USE_SCALE_SHIFT_NORM]
                            [--classifier_resblock_updown CLASSIFIER_RESBLOCK_UPDOWN]
                            [--classifier_pool CLASSIFIER_POOL]
classifier_sample.py: error: unrecognized arguments: --attention_resolutions 32,16,8 --class_cond True --diffusion_steps 1000 --dropout 0.1 --image_size 64 --learn_sigma True --noise_schedule cosine --num_channels 192 --num_head_channels 64 --num_res_blocks 3 --resblock_updown True --use_new_attention_order True --use_fp16 True --use_scale_shift_norm True
```
恼，然后用脚本试了试，发现了解决的办法:  

- 可以把参数直接复制下来不使用变量的方法，是可以的。  
- 用bash执行脚本，也不会有问题。  
- 如果还使用zsh和变量的话需要改为`"$FLAG"`，就好了  

算是个小坑吧,shell脚本是有点玄学在里面的，建议以后没事都加个双引号