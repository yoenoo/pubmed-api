import httpx
import xml.etree.ElementTree as ET
from typing import List, Dict
from dataclasses import dataclass
from datetime import datetime



BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"

def get_pubmed_ids(query: str) -> list[str]:
  params = dict(db="pubmed", term=query)
  url = BASE_URL + "/esearch.fcgi"
  r = httpx.get(url, params=params)
  r.raise_for_status()

  root = ET.fromstring(r.text)
  id_list = root.find(".//IdList")
  return [id_elem.text for id_elem in id_list.findall("Id")] if id_list is not None else []

@dataclass
class PubMedArticle:
  pmid: str
  href: str
  title: str
  abstract: str
  authors: List[Dict[str, str]]
  journal: Dict[str, str]
  pub_date: Dict[str, str]
  mesh_terms: List[str]
  doi: str = ""

def get_pubmed_doc_by_ids(pmids: list[str]) -> List[PubMedArticle]:
  params = dict(db="pubmed", id=",".join(pmids), retmode="xml")
  url = BASE_URL + "/efetch.fcgi"
  r = httpx.get(url, params=params)
  r.raise_for_status()

  root = ET.fromstring(r.text)
  articles = []
    
  for article in root.findall(".//PubmedArticle"):
    pmid = article.find(".//PMID").text
    doi = article.find(".//ArticleId[@IdType='doi']").text
    href = f"https://pubmed.ncbi.nlm.nih.gov/{pmid}"
    title = article.find(".//ArticleTitle").text
    abstract = article.find(".//Abstract/AbstractText").text 
    # abstract = "".join(x.text for x in list(article.find(".//Abstract/AbstractText")))
    # abstract = ET.tostring(article.find(".//Abstract/AbstractText"), encoding='unicode', method='xml')

    authors = []
    journal = {}
    pub_date = {}
    mesh_terms = []

    article = PubMedArticle(
      pmid=pmid,
      href=href,
      title=title,
      abstract=abstract,
      authors=authors,
      journal=journal,
      pub_date=pub_date,
      mesh_terms=mesh_terms,
      doi=doi
    )
    articles.append(article)

  return articles



    #     # Get PMID
    #     pmid = article.find(".//PMID").text
        
    #     # Get title
    #     title = article.find(".//ArticleTitle").text
        
    #     # Get abstract
    #     abstract = ""
    #     abstract_elem = article.find(".//Abstract/AbstractText")
    #     if abstract_elem is not None:
    #         abstract = abstract_elem.text or ""
        
    #     # Get authors
    #     authors = []
    #     for author in article.findall(".//Author"):
    #         author_info = {}
    #         if author.find("LastName") is not None:
    #             author_info["lastname"] = author.find("LastName").text
    #         if author.find("ForeName") is not None:
    #             author_info["forename"] = author.find("ForeName").text
    #         if author.find("Initials") is not None:
    #             author_info["initials"] = author.find("Initials").text
    #         if author.find("Affiliation") is not None:
    #             author_info["affiliation"] = author.find("Affiliation").text
    #         authors.append(author_info)
        
    #     # Get journal info
    #     journal = {
    #         "title": article.find(".//Journal/Title").text,
    #         "issn": article.find(".//Journal/ISSN").text,
    #         "volume": article.find(".//Journal/JournalIssue/Volume").text,
    #         "issue": article.find(".//Journal/JournalIssue/Issue").text,
    #     }
        
    #     # Get publication date
    #     pub_date = {
    #         "year": article.find(".//Journal/JournalIssue/PubDate/Year").text,
    #         "month": article.find(".//Journal/JournalIssue/PubDate/Month").text,
    #     }
        
    #     # Get MeSH terms
    #     mesh_terms = []
    #     for mesh in article.findall(".//MeshHeading/DescriptorName"):
    #         mesh_terms.append(mesh.text)
        
    #     # Get DOI
    #     doi = ""
    #     for article_id in article.findall(".//ArticleId"):
    #         if article_id.get("IdType") == "doi":
    #             doi = article_id.text
        
    #     articles.append(PubMedArticle(
    #         pmid=pmid,
    #         title=title,
    #         abstract=abstract,
    #         authors=authors,
    #         journal=journal,
    #         pub_date=pub_date,
    #         mesh_terms=mesh_terms,
    #         doi=doi
    #     ))
    
    # return articles

if __name__ == "__main__":
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument("--query", type=str, required=True)
  args = parser.parse_args() 

  pmids = get_pubmed_ids(args.query)
  print(f"fetched {len(pmids)} documents...")

  docs = get_pubmed_doc_by_ids(pmids)
  for doc in docs:
    print(f"PMID: {doc.pmid}")
    print(f"Link: {doc.href}")
    print(f"DOI: {doc.doi}")
    print(f"Title: {doc.title}")
    # print(f"Journal: {doc.journal['title']} {doc.journal['volume']}({doc.journal['issue']})")
    print(f"Authors", doc.authors)
    # print(f"Authors: {', '.join([f'{a["lastname"]} {a["initials"]}' for a in doc.authors])}")
    print(f"Abstract: {doc.abstract[:200]}...")
    # print(f"MeSH Terms: {', '.join(doc.mesh_terms)}")
    print("---\n")