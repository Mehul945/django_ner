import spacy
from spacy.matcher import Matcher
import csv
import pytesseract
from PIL import Image
import pandas as pd
import json

nlp = spacy.load("en_core_web_lg")
matcher = Matcher(nlp.vocab)
email_pattern = [
    {"TEXT": {"REGEX": r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b"}}]
phone_pattern = [{"TEXT": {"REGEX": r"\d{10}-"}}]

matcher.add("EMAIL", [email_pattern])
matcher.add("PHONE", [phone_pattern])


def extract_text_from_image(image,filename):
    text = pytesseract.image_to_string(Image.open(image))
    with open(f"result_files/{filename}.txt",'w+') as f:
        f.write(text)
    print(text)
    return text


def convert_doc(text):
    return nlp(text)


def extract_entities(doc,filename):
    details = {} 
    for ent in doc.ents:
        if ent.label_ == "CARDINAL":
            continue
        if ent.label_ == "ORG":
            ent.label_ = "COMAPNY"
        if ent.label_ not in details:
            details[ent.label_] = []
        details[ent.label_].append(ent.text)
    json.dump(details,open(f'result_files/{filename}.json','w+'))
    return details


def extract_contacts(doc):
    matches = matcher(doc)
    contacts = {}
    for match_id, start, end in matches:
        if nlp.vocab.strings[match_id] not in contacts:
            contacts[nlp.vocab.strings[match_id]] = []
        contacts[nlp.vocab.strings[match_id]].append(doc[start:end].text)
    json.dump(contacts,open('result_files/{filename}_contacts.json','w+'))
    return contacts


def extract_bank(sents):
    details = {}
    for i in sents:
        if "branch" in i.lower() and 'code' in i.lower():
            try:
                print("BRANCH CODE", i)
                details['branch_code'] = i.lower().split("branch code")[
                    1].split()[0].replace(":", '')
            except Exception as e:
                pass
        if "ifsc" in i.lower():
            try:
                details['ifsc'] = i.split(":")[1].split()[0]
            except Exception as e:
                pass
        if "date" in i.lower() and "issue" in i.lower():
            try:
                details['date of issue'] = i.lower().split("date of issue")[
                    1].split()[0].replace(":", '')
            except Exception as e:
                pass
        if 'phone' in i.lower():
            try:
                details['phone'] = i.lower().split('phone')[1].split(':')[1]
            except Exception as e:
                pass
        if 'name' in i.lower():
            try:
                details['Name'] = i.lower().split('name')[1].split(':')[1]
            except Exception as e:
                pass
        if 'address' in i.lower():
            try:
                details['Address'] = i.lower().split('address')[
                    1].split(":")[1]
            except Exception as e:
                pass
    return details
