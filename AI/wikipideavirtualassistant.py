import wolframalpha

question = input('Question: ')

app_id = 'GLJG2K-JY85JX64X9'

client = wolframalpha.Client(app_id)

res = client.query(question)

try:
    answer = next(res.results).text
    print("Answer: ", answer)
except StopIteration:
    print("No results found.")