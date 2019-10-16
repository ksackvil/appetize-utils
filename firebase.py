# import firebase_admin
# from firebase_admin import credentials
# from firebase_admin import firestore

# # Use the application default credentials
# cred = credentials.ApplicationDefault()
# firebase_admin.initialize_app()

# # reference to database
# db = firestore.client()

# # Des: sets document with body, if doc dne then it will create it
# # @Param: col = target collection (string)
# #         doc = target document (string)
# #         body = json object to write (object)
# #         or edit the existing object, else it will make a new obj.
# # Post: object is edited/created
# def write(col, doc, body):
#     # Add a new doc in collection 'col' with ID 'doc'
#     ref = db.collection(col)
#     ref.document(doc).set(body)


# # Des: fetches a specific document from firebase database given the 
# #       collection name and the document name
# # @Param: col = target collection (string)
# #         doc = target document (string)
# # Post: return the target document as type dict
# def getDoc(col, doc):
#     doc_ref = db.collection(col).document(doc)

#     try:
#         doc = doc_ref.get()
#         # print(u'Document data: {}'.format(doc.to_dict()))
#     except:
#         print(u'No such document!')
    
#     return doc.to_dict()