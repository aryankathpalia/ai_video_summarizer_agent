# Splitting the text into chunks and with overlap
def  chunk_text(text:str, chunk_size:int = 2000, overlap:int = 200) -> list:

    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = min(start + chunk_size, text_length)
        chunk = text[start:end]
        chunks.append(chunk)
        
        # move the start pointer, allowing for overlap if any
        start += chunk_size - overlap

        if start < 0:
            start = 0
    return chunks

# Summarizes large text by splitting it into chunks, summarizing each chunk, and combining those summaries into a final summary
def chunked_summarize(text:str,summarize_func, max_chunk_size:int = 2000) -> str:
    # 1. Split the text into chunks
    text_chunks = chunk_text(text, chunk_size=max_chunk_size, overlap=200)

    # 2. Summarize each chunk individually
    partial_summaries = [summarize_func(chunk) for chunk in text_chunks]

    # 3. Combine the partial summaries into a final summary
    combined_summary_imput = " ".join(partial_summaries)

    # 4. Run a final summarization on the combined summary
    final_summary = summarize_func(combined_summary_imput)
    return final_summary



