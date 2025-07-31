import pymupdf4llm
import pathlib
from langchain.text_splitter import MarkdownTextSplitter

md_text = pymupdf4llm.to_markdown("../data/eva.pdf")  # get markdown for all pages

splitter = MarkdownTextSplitter(chunk_size=100, chunk_overlap=20)

print(type(splitter.create_documents([md_text])))
