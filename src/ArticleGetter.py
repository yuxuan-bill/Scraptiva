from src import Search_v2


# firm_name: string representing the name of company
# role: the role to search for, can take on two values: 'CEO' and 'CFO'
# return: the resulting html files of articles that satisfy the search criteria, in the form of a list of strings
def get_article_pages(firm_name, role):
    try:
        return Search_v2.search(firm_name, role)
    except Exception:
        print("Something went wrong")
        return []
