from github import Github
token = Github('Kzt7f8pR9KONhlNSA0LmAEKYzsABzp03Xa4D')
repo = token.get_repo('JBufl/FPIBGUtility')
issues = repo.get_issues(state='all')
for issue in issues:
    print(issue.url)