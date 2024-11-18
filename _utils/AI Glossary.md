---
creation date: 2024-11-12
created: 2024-11-12 10:10
aliases: 
id: 01HMDEHWQ0WBKKNQVZFRZE5HYJ
updated: 2024-11-13T14:16:53-06:00
---

## 🏷️ #🌱

## 🔗created by: [[2024-11-12]]

---

## AI Glossary

Animate Diff: text-to-video Stable Diffusion SD1.5 based method that aims to enhance a pre-existing text-to-image model by adding a motion modeling module.
AudioCrafter: AudioCrafter is a model suite by MetaAI that can generate audio from text prompts, and is often used in conjunction with video generation workflows to create audio for generated videos.
Black Forest Labs: creators of Flux diffusion model family founded by former Stability AI employees
Captioning: The process of adding descriptive text to an image to provide context or information about the image content. Diffusion models are trained on image/caption pairs, allowing generative AI models to be "prompted" in text 2 image workflows. Captioning models perform the reverse of this, and can be considered an Image to Text pipeline. Common captioning methods used in Eden and the broader generative AI community include CLIP Interrogation and OpenAI's CLIP Captioning, Florence2 captioning model by Microsoft, DeepBooru tagging, GPT vision, and other "DocQA" image querying protocols. 
CFG: CFG stands for "Classifier Free Guidance" and is a setting in Stable Diffusion that controls how closely the AI-generated image follows the text prompt influence.
ChatGPT: A large language model developed by OpenAI, capable of understanding and generating human-like text based on input prompts.
Civitai: A platform for sharing and discovering machine learning models, LoRAs and other AI resources including ComfyUI workflows.
Claude: An AI language model developed by Anthropic, designed to assist with various natural language processing tasks similar to ChatGPT.
Checkpoint: A saved state of a machine learning model during training, allowing the training process to be resumed from that point if needed. In Stable Diffusion this often refers to community trained fine-tuned models distributed by platforms like Civitai.
CLIP: Contrastive Language-Image Pre-Training is a neural network model by OpenAI that connects images and text, enabling tasks like image captioning and zero-shot classification.
ClipVision: An extension or variant of the CLIP model focused specifically on vision-related tasks, enhancing image understanding and processing capabilities.
ComfyUI: ComfyUI is a node-based GUI for Stable Diffusion. You can construct an image generation workflow by chaining different blocks (called nodes) together. It is a free, open-source, web-based graphical user interface (GUI) by Comfyanonymous (Comfyui.org) that allows users to create and modify AI generation tasks widely used by the community to create "workflows" of "nodes" chained together to automate AI generation tasks.
Conditioning Scale: A parameter that controls the strength or influence of conditioning inputs (such as prompts or auxiliary data) on the output of a generative model.
Configuration (CFG): Settings or parameters that define the behavior and properties of a machine learning model or software application.
ControlNet: ControlNet is a collection of models that can be used to control the Diffusion image generation process. It adds extra conditions to the default Stable Diffusion models, allowing users to have more control over the images generated. On Eden we refer to a shape guidance input image, which is the source for conditioning the image generation.
Controlnet Preprocessors: Modules that prepare input data for ControlNet, ensuring it is in the correct format and structure for processing. Examples include:
- Canny: An edge detection algorithm used to highlight prominent edges in images, producing a thin binary edge map. While fast, Canny is sensitive to noise and not very good at prioritizing and preserving relevant details.
- Depth: Preprocessing that involves estimating the depth information of an image, producing a luminance depth map in which "closer" objects are brighter.
- HED: Holistically-Nested Edge Detection, a method for detecting edges in images. Hed is very good for intricate details and outlines. It produces soft, smooth outlines that are more noise-free than Canny and also preserves relevant details better, at the cost of being slower.
- OpenPose: A library for real-time multi-person keypoint detection, useful for human pose estimation.
- LineArt: A preprocessor that converts images into line drawings or outlines. This controlnet is better suited for line art images, cartoons, manga, and other images that have a strong black and white contrast.
- Scribble: A preprocessor that converts rough sketches or scribbles into structured inputs for models. This controlnet is better suited for images that have a rough, sketchy appearance, and produces thicker rough sketch lines than the LineArt controlnet.
Controlnet Strength: A parameter that adjusts the degree to which ControlNet influences the generation process, controlling the influence strength of a controlnet shape guidance input on the image generation.
DeepBooru: "DeepDanBooru" is a popular image tag estimation system that uses a combination of CLIP and a Booru-style models to generate captions for images. Popular in the anime space, these tags are comma separated descriptive tokens stripped of natural language context that can be useful for prompt guidance of older diffusion models such as SD1.5 and SDXL.
Denoise: Denoising strength (often called Generation Strength or AI Creativity in Eden tools) determines how much noise is added to an image before the sampling steps. It is a common setting in image-to-image applications in Stable Diffusion. The value of denoising strength ranges from 0 to 1. 0 means no noise is added to the input image. 1 means the input image is completely replaced with noise, which is the default setting when generating from pure text without any input image conditioning.
Depth Map: A luminance map depth estimation of an image that conveys information about the distance of objects from the viewpoint, used in 3D rendering and computer vision, in which "closer" objects are represented as brighter pixels.
Diffusion Models: A class of generative models that use a stochastic process to generate data, typically images, by iteratively refining a noisy version of the desired output.
Embedding: Embedding is the result of textual inversion, a method to define new keywords in a model without modifying it. A vector representation of a word or phrase (token), capturing its semantic meaning and context in a numerical format. In the context of of trained LoRAs, a custom embedding is used to associate the LoRA weights to a token sequence invoked in the prompt. The method has gained attention because its capable of injecting new styles or objects to a model with as few as 3 -5 sample images
Encoder: A neural network module that converts input data into a a dense (latent space) representation, arranging similar data points closer together in an abstract space, which can be used for efficient processing and analysis.
FILM: Frame Interpolation for Large Motion is a technique for generating smooth video transitions by interpolating between frames of a video. Similar to RIFE, FILM uses a temporal encoder to encode the input video frames into a latent space representation, and then uses a temporal decoder to interpolate between the encoded frames to generate a smooth video.
Fine-Tuning: The process of adjusting a pre-trained model to improve its performance on a specific task or dataset. In the context of Stable Diffusion checkpoints, this often refers to taking a pre-trained Stable Diffusion model that's already seen countless images and learned the basics of image generation, and giving it additional training focused on a specific curated dataset.
Florence2: a lightweight vision-language foundation model developed by Microsoft Azure AI and open-sourced under the MIT license. It aims to achieve a unified, prompt-based representation for diverse vision and vision-language tasks, including captioning, object detection, grounding, and segmentation.
Flux: A family of diffusion models created by Black Forest Labs. Flux models are known for their high-quality outputs, prompt adherence, and ability to accurately generate text, and comes in 3 variants: Flux-Dev, Flux-Schnell, an open license fast distilled variant, and Flux-Pro, a closed license high quality model. Flux notably employs the T5 text encoder in addition to CLIP, which allows for more conversational human-like natural language prompting, and was trained on images with resolutions ranging from 0.1 to 2.0 megapixels, allowing for a wide range of image generation output sizes without artifacting.
Frame Interpolation: Frame Interpolation is a technique for generating intermediate frames between two existing image or video frames, creating a smooth transition between them.
Guidance Scale: A parameter that controls the strength of the conditioning input (prompt) on the generated image. Higher guidance scale values allow the model to generate images more closely matching the text prompt, while lower values make the model more likely to generate images with a wider variety of styles and details.
HelloMeme: highly accurate facial expression transfer model that applies the facial expression from a control image or video to a video sequence.
Img2Img: An image-to-image workflow that generates an image based on guidance from an input image and a text prompt, often using Stable Diffusion or Flux models.
Img2Vid: An image-to-video workflow that generates a video based on guidance from an input image and a text prompt, often using AnimateDiff stable diffusion, Stable Video Diffusion, RunwayML Gen3, or other video generation models.
Inference: AI inference is when an AI model produces predictions or conclusions based on input data. In the context of AI workflows, inference refers to the process of generating output data from input data using an AI model.
Inpainting: Inpainting is a technique for filling in missing parts of an image with generated content, often used to remove unwanted objects or replace details from in an image. This method typically uses a mask to define the area to be inpainted, and then prompt based image generation to fill in the missing parts.
Input Image: The image used as a conditioning input for image generation workflows.
Insightface: A face detection model that can identify and locate faces in images, and extract facial features such as landmarks and facial attributes.
IP-Adapter: IP-Adapter is an image prompt adapter that can be plugged into diffusion models to enable image prompting without any changes to the underlying model. Its main use is to enable prompting from an input image instead of or in addition to text. This input is often referrenced on Eden as a "style image". 
Latent Space: A latent space is a lower-dimensional representation of high-dimensional data that captures the underlying factors that explain the data's variability. It's also known as a latent feature space or embedding space
LayerDiffuse: an approach enabling large-scale pretrained latent diffusion models to generate transparent images, employed by the Eden tool "Create an image with transparency"
LCM: Latent Consistency Models (LCMs) enable fast high-quality image generation by directly predicting the reverse diffusion process in the latent rather than pixel space. In other words, LCMs try to predict the noiseless image from the noisy image in contrast to typical diffusion models that iteratively remove noise from the noisy image. By avoiding the iterative sampling process, LCMs are able to generate high-quality images in 2-4 steps instead of 20-30 steps.
Learning Rate: Learning rate is a parameter that controls the step size of the gradient descent optimization process in machine learning model training. It determines how much the model parameters are updated per step during training. A higher learning rate can lead to faster convergence, while a lower learning rate may result in better generalization at the expense of slower convergence.
LivePortrait: Live Portrait is a face swap model that can replace the face of a person in an image with a different face from a control image or video.
LLM: Large Language Models (LLMs) are a type of AI model that can understand and generate human-like text based on input prompts. They are typically pre-trained on vast amounts of text data and can be fine-tuned for specific tasks like natural language processing, question answering, and more.
LoRA (Low-Rank Adaptation): LoRA is a technique for adapting pre-trained models to specific tasks or datasets by adding low-rank matrices to the model's weights, allowing for efficient fine-tuning without the need to retrain the entire model. In the context of Eden, LoRAs are referred to as "custom models", allowing a user to train a new concept based on a small curated dataset of several images. This allows users to invoke a person, style or concept in their generation workflows, great for creating custom avatars, incorporating personal styles, or preserving one's own face in generated images.
LoRA trainer: A tool in Eden that allows a user to train a custom LoRA model based on a small curated dataset of several images.
Mask: A mask is a binary (black and white) image or image sequence that defines the area to be inpainted or used for other masking based image processing tasks.
Mochi: Mochi 1 preview is an open weight permissive Apache 2.0 licensedstate-of-the-art video generation model with high-fidelity motion and strong prompt adherence
Model: A machine learning model, including pre-trained image generation models like Stable Diffusion, is the base checkpoint that is used as a starting point for AI inference.
Motion Brush: a Motion Brush is a tool that works with certain video generation models by allowing users to add controlled movement to their video outputs, allowing users to “paint” an area or subject, choosing a direction and intensity to add motion to that area by the defined degree.
MusicGen: MusicGen is a model by MetaAI, part of the AudioCrafter suite, that can generate music from text prompts, and is often used in conjunction with video generation workflows to create audio for generated videos.
Negative Prompt: A prompt that is used to guide the AI model away from certain aspects or subjects, often used to remove unwanted elements or styles from the generated image.
Nodes: Modules in a node-based GUI architecture like ComfyUI that perform specific tasks, such as image generation, processing, or manipulation.
Object Detection: Object Detection is a technique for identifying and locating objects within an image, and can be used to detect or identify specific objects or categories of objects, as well as draw bounding boxes around detected objects and return their coordinates within the canvas of an image.
OpenAI: OpenAI is the company that created the CLIP model, ChatGPT, and DALL-E image generation models, and is a driving force in the development of the generative AI models, architectures and technologies.
Outpainting: Outpainting is a technique for generating additional content beyond the edges of an image, often used to expand the canvas of a supplied input image.
PingPong: PingPong is a common vernacular for a forwards-backwards loop, often used in video generation workflows to create a looped video by appending a generated video with its reverse.
Prompt Engineering: Prompt engineering is the process of refining and optimizing text prompt inputs to guide AI models to generate desired outputs. It involves crafting clear, specific, and context-aware prompts to influence the AI model's behavior and produce more accurate and relevant results. CLIP based text encoder models like SD1.5 and SDXL rely on verbose "tag" style prompts to guide generation by invoking concepts, styles and quality modifiers, while newer models like Flux and SD3 also incorporate the T5 text encoder, which allows for more conversational human-like natural language prompting.
RIFE: Real-Time Intermediate Flow Estimation is a video interpolation model that can generate intermediate frames between two existing video frames, creating a smooth transition between them. On Eden this is used in many video generation tools, and exists as a standalone tool in the Keyframe Interpolation and Slow Motion video workflows to extend the length of a video.
RunwayML: is a company that specializes in generative artificial intelligence research and technologies, and is the creator of the RunwayML Gen3 video generation model.
Stable Audio: Stable Audio is a model that can generate audio from text prompts, and is often used in conjunction with video generation workflows to create audio for generated videos.
Stable Video Diffusion: Stable Video Diffusion is an open weight video generation model by Stability AI that can generate short videos from text prompts, and is often used in conjunction with image generation workflows to create moving image AI content.
SD1.5: Stable Diffusion 1.5 is the first gen pre-trained image generation model by Stability AI that can generate images from text prompts, and is often used in conjunction with image generation workflows to create images with a variety of styles and details. Still adored for its unique style, quality, and range of relatively uncensored training data, SD1.5 is now surpassed by newer models like SDXL. For Stable Diffusion 1.5, outputs are optimised around 512x512 pixels, and produces identifiable artifacts at other resolutions.
SDXL: Stable Diffusion XL, the successor to SD1.5, is an open source image generation model by Stability AI that can generate high-quality images from text prompts, and is at the time of this writing the most developed image generation architecture due to extensive community development and proliferation of finetuned model checkpoints, and supplemental tools like Controlnet and Ipadapters. SDXL was trained on images around 1024x1024 pixels in size (1 megapixel), and is optimised for generation at this resolution.
SD3: Stable Diffusion 3 and its successor SD3.5 are newer image generation models by Stability AI that can generate high-quality images from text prompts, and most notably employs the T5 text encoder in addition to CLIP, which allows for more conversational human-like natural language prompting. SD3 and SD3.5 were trained on images around 1024x1024 pixels in size (1 megapixel), and are optimised for generation at this resolution.
Seed: A seed is a random number used to initialise a pseudo-random number generator, which is used to create repeatable results in image generation workflows. By default a random seed is generated for each generation, but a user can also specify a seed number to return the same result, or iterate on a result by locking the seed and adjusting the text prompt and other parameters.
Segment Anything (SAM): Segment Anything is a model developed by Meta AI that can segment objects in images, and is often used in conjunction with image generation workflows to create detailed masks for inpainting and other image processing tasks.
Stability AI: Stability AI is the company that created the Stable Diffusion image generation model, and is a notable contributor to the development of the the opensource generative AI community.
Steps: Steps is a parameter that controls the number of diffusion steps taken to generate an image, with each step iteratively refining the image towards the desired output. Higher steps result in more detailed and accurate images, but also increase the computational cost and time required for generation.
StreamDiffusion: StreamDiffusion is an innovative diffusion pipeline designed for real-time interactive generation, allowing users to quickly batch generate images with text prompts in rapid succession.
Style Transfer: Style Transfer is a technique for applying the style of one image to another image, often used to transfer the shape or style of an input image to a generated output.
Pre-trained model: A pre-trained model is a machine learning model that has been trained on a large dataset and is ready for use on a specific task, without the need for additional training.
Prompt: A prompt is a text input used to guide the AI model to generate a desired output. Prompts can be used to guide the generation process, constrain the output, or influence the style and quality of the generated image.
Quantized Models: Quantized models are machine learning models that have been compressed to reduce their size and improve their computational efficiency, often at the cost of some loss in model accuracy. Popular for their ability to run on consumer hardware, LLMs and image generation models are often pruned and quantized by the community to make them more accessible to a wider audience.
RealESRGAN: RealESRGAN is a super-resolution model that can upscale images to a higher resolution, improving the quality of low-resolution images. It is one of many popular upscaling models employed in Eden to improve the quality of generated images.
Resolutions: Resolutions refer to the width and height size of an image generated by an AI model, often measured in pixels. Common resolutions include 512x512, 1024x1024, and 2048x2048 pixels. Higher resolutions generally produce more detailed and accurate images, but also require more computational power and time to generate. Generative AI models were trained on data sets at particular resolutions, and are optimised for creations at those dimensions, often producing noticeable artifacts resolutions outside of the dimensions they were trained on.
T5: A family of Transformer-based models developed by Google for natural language processing tasks, including text-to-text generation. Contrary to older image generation models like SD1.5 and SDXL that only rely on CLIP caption based text conditioning, models like Flux and SD3 also employ T5 which allows for a more conversational human-like prompting.
Tensor: A data structure used in machine learning to store and manipulate numerical data, often in multi-dimensional arrays.
Text2Image: Text2Image is an image generation workflow that can generate an image based on a text prompt, often using Stable Diffusion or Flux models.
Text2Video: Text2Video is a video generation workflow that can generate a video based on a text prompt, often using AnimateDiff stable diffusion, Stable Video Diffusion, RunwayML Gen3, or other video generation models.
Token: A unit of data in a sequence, representing a word or part of a word in a text.
ToonCrafter: ToonCrafter is a generative cartoon interpolation model that seamlessly transforms static images into fluid animations by leveraging the pre-trained image-to-video diffusion priors.
VAE (Variational Autoencoder): A variational autoencoder (VAE) is a generative model in machine learning that uses deep learning to create new data that's similar to the training data. VAEs are made up of two neural networks, an that compresses the input data into a smaller representation, and a decoder that uses the latent representation to reconstruct the original input. VAEs are a foundational component of all diffusion model pipelines, decoding the latent image into a usable pixel space. 
Weight: In the context of machine learning, a weight is a parameter in a model that determines the strength of a particular feature or aspect of the model's output. Weights are adjusted during the training process to optimize the model's performance on a specific task.




### Backlinks  

```dataview  
LIST  
FROM [[AI Glossary]]  
WHERE !contains(tags, "waypoint")  
AND !contains(file.name, "_")  
AND !contains(file.name, "+")  
AND !contains(file.name, "%")  
AND !contains(file.path, "Daily Notes")  
```
