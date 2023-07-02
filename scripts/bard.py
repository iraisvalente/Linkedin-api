import requests

from bardapi import Bard

def bard(company, position):
    name=""
    token = "XwiDpXiEhijX8nBBPIgQFuUPrsR6hvyruO9IqE4pnxBToQ4PmqaeSa39453EbIn0mvcU4w."
    question = f"{company}  {position}"
    try:
        bard = Bard(token=token)
        answer= bard.get_answer(question)['content']
        if "Error" in answer:
            return {"answer": answer}
    except Exception as e:
        if "Check __Secure-1PSID" in str(e):
            return {"answer": "Secure-1PSID ::: Invalid"}
    try:
        answer_list=answer.split(".")
        correct_answer= [x for x in answer_list if f"{company.upper()}" in x.upper() and  f"{position.upper()}" in x.upper() and  "IS" in x.upper()]
        complete_answer = ''.join(correct_answer)
        name = correct_answer[0]
        name = name.split("is")
        name = [y for y  in name if "THE" not in y.upper()]
        Real_answer = name[0].strip() + ".\n" + complete_answer  
        print(Real_answer)
        try:
            name=name[0].split(" ")
            name= '+'.join(x for x in name)[1:]
            search= f"https://google.com/search?q={name}+linkedin&btnI=I%27m+Feeling+Lucky&source=hp"
            response=requests.get(search)
            link=response.text.split('<a href="')[1].split('"')[0]
            print(f"Linked in link: {link}")
            return {"answer": f"{Real_answer}\n{link}"}
        except:
            return {"answer": "Error at searching with bard"}
    except:
        return {"answer": "Error at searching with bard"}
        