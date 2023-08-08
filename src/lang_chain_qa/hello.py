# https://www.markhneedham.com/blog/2023/06/23/hugging-face-run-llm-model-locally-laptop/

import os
import torch

from langchain.llms import HuggingFacePipeline
from langchain import PromptTemplate, LLMChain

assert len(os.environ["HUGGINGFACEHUB_API_TOKEN"]) > 0

# choose GPU or CPU
# TODO: fix error "CUDA out of memory. Tried to allocate 40.00 MiB (GPU 0; 3.81 GiB total capacity; 3.36 GiB already allocated; 26.38 MiB free; 3.37 GiB reserved in total by PyTorch) If reserved memory is >> allocated memory try setting max_split_size_mb to avoid fragmentation.  See documentation for Memory Management and PYTORCH_CUDA_ALLOC_CONF"
# device = torch.cuda.current_device() if torch.cuda.is_available() else -1
device = -1

# the model will be downloaded on first use, if not cached in ~/.cache/huggingface/hub/
model_id = "lmsys/fastchat-t5-3b-v1.0"
model = HuggingFacePipeline.from_model_id(
    model_id=model_id,
    task="text2text-generation",
    model_kwargs={"temperature": 0, "max_length": 1000},
    device=device
)

text_template = """
You are a friendly chatbot assistant that responds conversationally to users' questions.
Keep the answers short, unless specifically asked by the user to elaborate on something.

Question: {question}

Answer:"""

prompt_template = PromptTemplate(template=text_template, input_variables=["question"])

llm_chain = LLMChain(prompt=prompt_template, llm=model)

question = "Who is Sheryl Crow?"
print(llm_chain(question))
