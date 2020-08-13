import os

BASEDIR = os.path.dirname(os.path.abspath(__file__))

# DIRS = []
# for root, dirs, files in os.walk(BASEDIR):
#     for dir in dirs:
#         finalPath = os.path.join(root, dir)
#         if '__pycache__' in finalPath:
#             continue
#         if '.idea' in finalPath:
#             continue
#         DIRS.append(finalPath)
# for dir in DIRS:
#     print dir

FILES = []
for root, dirs, files in os.walk(BASEDIR):
    for file in files:
        finalPath = os.path.join(root, file)
        if '__pycache__' in finalPath:
            continue
        if '.idea' in finalPath:
            continue
        if '__init__.py' in finalPath:
            continue
        if finalPath.endswith('.py'):
            FILES.append(finalPath)
for file in FILES:
    print file


    # for file in files:
    #     print file
