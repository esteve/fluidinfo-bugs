from github3 import client

def close_milestone(username=None, password=None, repo_user='fluidinfo',
                    repo_name='fluiddb', old_milestone_name=None,
                    new_milestone_name=None):
    """
    Close a milestone.
 
    Connect to Launchpad and move all bugs in the old milestone that aren't
    marked as 'Fix Committed' or 'Fix Released' to the new milestone.  Bugs
    that are marked as 'Fix Committed', 'Fix Released', 'Invalid' or 'Won't
    Fix' are left in the old milestone.  If you haven't already done so, run
    the launchpad-login command to create OAuth credentials.
    """ 
    c = client.Client(username=username, password=password)
    repo = client.Repo(c, repo_user, repo_name)
    milestones = repo.milestones()
    old_milestone = None
    new_milestone = None
    for milestone in milestones:
        if milestone['title'] == old_milestone_name:
            old_milestone = milestone
        if milestone['title'] == new_milestone_name:
            new_milestone = milestone
    if not old_milestone:
        raise Exception("Can't find milestone %s" % old_milestone_name)
    if not new_milestone:
        new_milestone = milestones.append(title=new_milestone_name)
    issues = repo.issues(milestone=old_milestone['number'], state='open')
    for issue in issues:
        issue.update({'milestone': new_milestone['number']})

def release_milestone(username=None, password=None, repo_user='fluidinfo',
                      repo_name='fluiddb', milestone_name=None):
    """
    Release a milestone.

    Connects to Launchpad and marks all 'Fix Committed' bugs in the milestone
    as 'Fix Released'.  Bugs that aren't marked as 'Fix Committed' are left in
    the milestone in the whatever state they're in.  The milestone's active
    flag is set to false to hide it on bug forms in Launchpad.  If you haven't
    already done so, run the launchpad-login command to create OAuth
    credentials.
    """
    c = client.Client(username=username, password=password)
    repo = client.Repo(c, repo_user, repo_name)
    milestones = repo.milestones()
    release_milestone = None
    for milestone in milestones:
        if milestone['title'] == milestone_name:
            release_milestone = milestone
    if not release_milestone:
        raise Exception("Can't find milestone")
    issues = repo.issues(milestone=release_milestone['number'], state='closed')
    for issue in issues:
        issue_labels = issue['labels']
        fix_release = False
        for issue_label in issue_labels:
            if issue_label['name'] == 'Fix Released':
                fix_release = True
        if not fix_release:
            issue_labels.append('Fix Released')
        issue.update({'labels': issue_labels})
    release_milestone.update({'state': 'closed'})
