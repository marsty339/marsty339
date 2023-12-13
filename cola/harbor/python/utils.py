import re
from functools import partial
from multiprocessing.dummy import Pool as ThreadPool


# return a list of filter repositories
# TODO: concurrency will speed up here
def filter_by_regex(repo_name, harbor_client, expression):
    # "v\d{1,3}\.\d{1,4}\.\d{1,5}" for release version
    # ".*-pr-.*" for pr version
    print("filtering repo %s ..." % repo_name)
    image_list = []
    tag_list = harbor_client.get_tags(repo_name)
    for tag in tag_list:
        if "name" in tag and re.compile(expression).match(tag["name"]):
            image_list.append(repo_name + ":" + tag["name"])
        else:
            continue
    return image_list


# get all filtered images list
def get_filtered_images(harbor_client, expression):
    repos_list = []

    # get all projects
    projects = harbor_client.get_projects()
    projects_ids = [project["project_id"] for project in projects]

    repos = concurrency(harbor_client.get_repositories, 8, projects_ids)
    flat_repos = [item for sublist in repos for item in sublist]
    for repo in flat_repos:
        if repo["name"]:
            repos_list.append(repo["name"])
        else:
            continue
    print("Scanned %s repositories in the harbor(%s)." % (len(repos_list), harbor_client.domain))

    filter_by_regex_repo = partial(filter_by_regex, harbor_client=harbor_client, expression=expression)
    image_list = concurrency(filter_by_regex_repo, 4, repos_list)
    flat_list = [item for sublist in image_list for item in sublist]

    print("Find %s tags matched regular expression %s" % (len(flat_list), expression))
    return flat_list


def delete_images(harbor_client, image_list):
    count = 0
    for image in image_list:
        if harbor_client.delete_by_tag(image.split(":")[0], image.split(":")[1]):
            print("Delete %s successfully." % image)
            count += 1
    print("Deleted %d images  successfully." % count)


def concurrency(fn, works, lists):
    pool = ThreadPool(works)
    results = pool.map(fn, lists)
    pool.close()
    pool.join()
    return results


def write_to_file(filename, images):
    with open(filename, "w") as f:
        f.writelines("%s\n" % image for image in images)


def read_from_file(filename):
    with open(filename, "r") as f:
        return f.read().splitlines()
