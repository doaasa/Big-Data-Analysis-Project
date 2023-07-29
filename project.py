import pandas as pd
from pymongo import MongoClient
import streamlit as st
from streamlit_option_menu import option_menu
import matplotlib.pyplot as plt
import seaborn as sns
import json



plt.rcParams['figure.max_open_warning'] = 50
st.set_page_config(layout="wide")


client = MongoClient('mongodb://localhost:27017/')
db = client['Drugs_Effect']
bio_decagon_combo1 = db['bio_decagon_combo']
decagon_effect1 = db['bio_decagon_effectcategories']
decagon_mono1 = db['bio_decagon_mono']
decagon_ppi1= db['bio_decagon_ppi']
targets1= db['bio_decagon_targets']
targetsall1= db['bio_decagon_targets_all']
gene_ass1= db['gene_associations']
disease_ass1= db['disease_associations']

combo= pd.read_csv('E:/مواد سنة رابعة/2nd trem/Big data/project/DPI_Dataset/DPI Project/Big-Data-Analysis-Project/Data/bio-decagon-combo.csv')
targets= pd.read_csv('E:/مواد سنة رابعة/2nd trem/Big data/project/DPI_Dataset/DPI Project/Big-Data-Analysis-Project/Data/bio-decagon-targets.csv')
gene_ass = pd.read_csv('E:/مواد سنة رابعة/2nd trem/Big data/project/DPI_Dataset/DPI Project/Big-Data-Analysis-Project/Data/gene_associations.tsv', delimiter='\t')
disease_ass= pd.read_csv('E:/مواد سنة رابعة/2nd trem/Big data/project/DPI_Dataset/DPI Project/Big-Data-Analysis-Project/Data/disease_associations.tsv',delimiter='\t' )


################### Find Quaries######################

def search_Side_Effect_Name_combo(Side_Effect_Name):
    # Use the find function to search for text in MongoDB
    results = bio_decagon_combo1.find({"Side Effect Name": {'$regex': f'.*{Side_Effect_Name}.*', '$options': 'i'}},{"_id":0})
    # Convert the results to a DataFrame!
    df = pd.DataFrame(list(results))
    
    return df

def search_Side_Effect_Name_cattegory_First_One(Side_Effect_Name):
  
      disease=decagon_effect1.find({"Side Effect Name":Side_Effect_Name},{"_id":0})
      df = pd.DataFrame(list(disease))
      return df

def Side_Effect_Related_Disease_Data(Side_Effect_Name):
    disease=disease_ass1.find({"diseaseId":Side_Effect_Name},{"_id":0})
    df = pd.DataFrame(list(disease))
    return df

def Find_Gene_Associations_Data(Gene_Name):
    #document1= targets1.find_one({"Gene":Gene_Name},{"_id":0})["Gene"]
    gene=gene_ass1.find({"geneId":int(Gene_Name)})
    df = pd.DataFrame(list(gene))
    return df

def disease_ass_searchName(Dis_name):
    gene=disease_ass1.find_one({"diseaseName":input("disease name")})
    df = pd.DataFrame(list(gene))
    return df

################### Insert Quaries######################

def Insert_PPI(gene1,gene2):
    d=decagon_ppi1.insert_one({"Gene 1":int(gene1),"Gene 2":int(gene2)})
    if (d.acknowledged==True):
        return 1
    else:
        return 0


def Inser_Combo(stitch1,stitch2,polID,polName):
    d=bio_decagon_combo1.insert_one({"STITCH 1":stitch1,"STITCH 2":stitch2,"Polypharmacy Side Effect":polID,"Side Effect Name":polName})
    if (d.acknowledged==True):
        return 1
    else:
        return 0
    
def Insert_Effect(sideID,sideName,DiseasClass):
    d=decagon_effect1.insert_one({"Side Effect":sideID,"Side Effect Name":sideName,"Disease Class":DiseasClass})
    if (d.acknowledged==True):
        return 1
    else:
        return 0
    
def Insert_Mono(stitchID,polID,polName):
    d=decagon_mono1.insert_one({"STITCH":stitchID,"Side Effect Name":polID,"Individual Side Effect":polName})
    if (d.acknowledged==True):
        return 1
    else:
        return 0

def Insert_Target(stitchID,GeneID):
    d=targets1.insert_one({"STITCH ":stitchID,"Gene":int(GeneID)})
    if (d.acknowledged==True):
        return 1
    else:
        return 0
    
def Insert_Target_All(stitchID,GeneID):
    d=targetsall1.insert_one({"STITCH ":stitchID,"Gene":int(GeneID)})    
    if (d.acknowledged==True):
        return 1
    else:
        return 0

def Insert_Gene_Associations(geneID,geneSymbol,protein_class_name):
    d=gene_ass1.insert_one({"geneId ":int(geneID),"geneSymbol":geneSymbol,"protein_class_name":protein_class_name})    
    if (d.acknowledged==True):
        return 1
    else:
        return 0      
        
    
def Insert_Disease_Associations(disID,disName,disType):
    d=disease_ass1.insert_one({"diseaseId":disID,"diseaseName":disName,"diseaseType":disType})    
    if (d.acknowledged==True):
        return 1
    else:
        return 0  

##########################UPDATE#########################
def Update_PPI(gene1,gene2):
    d=decagon_ppi1.update_one({"Gene 1":int(gene1)},{"$set": { "Gene 1": int(gene2) }})
    if (d.acknowledged==True):
        return 1
    else:
        return 0


def Update_Effect(DisclassOLD, DisclassNew):
    d=decagon_effect1.update_many({"Disease Class":DisclassOLD},{"$set":{"Disease Class":DisclassNew}})
    if (d.acknowledged==True):
         return 1
    else:
         return 0

def Update_Gene_Association(geneID, DisNO):
    d=gene_ass1.update_one({"geneId":int(geneID)},{"$set":{"NofDiseases": int(DisNO)}})
    if (d.acknowledged==True):
         return 1
    else:
         return 0
     
        
def Update_Target(stitchID,GeneID):
    d=targets1.update_one({"STITCH":stitchID},{"$set":{"Gene":int(GeneID)}})
    if (d.acknowledged==True):
         return 1
    else:
         return 0    
     
#################DELETE#################33
def Delete_Decagon(stitch1ID):
    d=bio_decagon_combo1.delete_many({"STITCH 1":stitch1ID})
    if (d.acknowledged==True):
         return 1
    else:
         return 0
        
def Delete_Decagon2(poly_side_effect):
    d=bio_decagon_combo1.delete_one({"Polypharmacy Side Effect":poly_side_effect})
    if (d.acknowledged==True):
         return 1
    else:
         return 0
     
def Delete_Decagon_Effect1(side_effect_name):
    d=decagon_effect1.delete_one({"Side Effect Name":side_effect_name})

    if (d.acknowledged==True):
         return 1
    else:
         return 0
        
def Delete_Decagon_ppi1(gene_1):
    d=decagon_ppi1.delete_many({"Gene 1":int(gene_1)})

    if (d.acknowledged==True):
         return 1
    else:
         return 0

def Delete_Decagon_Mono1(stitchID):
    d=decagon_mono1.delete_many({"STITCH":stitchID})

    if (d.acknowledged==True):
         return 1
    else:
         return 0
     
def Delete_Target(stitchID):
    d=targets1.delete_many({"STITCH":stitchID})

    if (d.acknowledged==True):
         return 1
    else:
         return 0
     
def Delete_Targetsall1(GeneID):
    d=targetsall1.delete_one({"Gene":int(GeneID)})

    if (d.acknowledged==True):
         return 1
    else:
         return 0

def Delete_Disease_ass2(disease_semantic_type):
    d=disease_ass1.delete_many({"diseaseSemanticType":disease_semantic_type})

    if (d.acknowledged==True):
         return 1
    else:
         return 0
        
def Delete_Disease_ass1(disease_name):
    d=disease_ass1.delete_many({"diseaseName":disease_name})

    if (d.acknowledged==True):
         return 1
    else:
         return 0
     
def Delete_Disease_ass3(disease_class):
    d=disease_ass1.delete_many({"diseaseClass":disease_class})

    if (d.acknowledged==True):
         return 1
    else:
         return 0
        
def Delete_Gene_ass1(protein_class_name):
    d=gene_ass1.delete_many({"protein_class_name":protein_class_name})

    if (d.acknowledged==True):
         return 1
    else:
         return 0
     
def Delete_Decagon_Effect_Bridge(Polypharmacy_Side_Effect):
        d=bio_decagon_combo1.delete_one({"Polypharmacy Side Effect":Polypharmacy_Side_Effect})
        c=decagon_effect1.delete_one({"Side Effect":Polypharmacy_Side_Effect})

        if (d.acknowledged==True and c.acknowledged== True):
             return 1
        else:
             return 0   
         
############Aggregations############
def agg_mono():
        # perform an aggregation query
    pipeline = [
        {
            '$group': {
                '_id': '$STITCH',  # group by Gene1 field
                'Side Effect count': {'$sum': 1}  # count the number of occurrences
            }
        },{
        '$project': {
            'STITCH': '$_id',  # rename _id field to grouping_criteria
         # include the total field
        "_id":0,    'Side Effect count': 1,
        }},
        {
            '$sort': {'Side Effect count': -1}  # sort by count in descending order
        }
    ]
    
    result = decagon_mono1.aggregate(pipeline)
    df = pd.DataFrame(list(result))
    last_col = df.pop(df.columns[-1])  # remove the last column from the DataFrame
    df.insert(0, last_col.name, last_col)
    return df

def agg_disType():
    # perform an aggregation query
    pipeline = [
        {
            '$group': {
                '_id': '$diseaseType',  # group by diseaseName field
                'diseaseSemanticType': {'$addToSet': '$diseaseSemanticType'}  # add geneSymbols to a set
            }
        },{
        '$project': {
            'Disease Type': '$_id',  # rename _id field to grouping_criteria
           # include the total field
        "_id":0,
        'diseaseSemanticType': 1
        }},
        {
            '$sort': {'Disease Type': 1}  # sort by diseaseName in ascending order
        }
    ]
    
    result = disease_ass1.aggregate(pipeline)
    df = pd.DataFrame(list(result))
    last_col = df.pop(df.columns[-1])  # remove the last column from the DataFrame
    df.insert(0, last_col.name, last_col)
    return df

def agg_disClass():
    pipeline = [
        {
            '$group': {
                '_id': '$diseaseClass',  # group by diseaseName field
                'diseaseSemanticType': {'$addToSet': '$diseaseSemanticType'}  # add geneSymbols to a set
            }
        },{
        '$project': {
            'Disease Class': '$_id',  # rename _id field to grouping_criteria
             # include the total field
        "_id":0,'diseaseSemanticType': 1
        }},
        {
            '$sort': {'diseaseSemanticType': 1}  # sort by diseaseName in ascending order
        }
    ]
    
    result = disease_ass1.aggregate(pipeline)
    df = pd.DataFrame(list(result))
    last_col = df.pop(df.columns[-1])  # remove the last column from the DataFrame
    df.insert(0, last_col.name, last_col)
    return df

def agg_Gennum():
    pipeline = [
        {
            '$group': {
                '_id': '$diseaseType',  # group by diseaseName field
                'Number of Genes': {'$sum': '$NofGenes'}  # add geneSymbols to a set
            }
        },{
        '$project': {
            'Disease Type': '$_id',  # rename _id field to grouping_criteria
        "_id":0,            'Number of Genes': 1  # include the total fie
        }},
        {
            '$sort': {'Number of Genes': -1}  # sort by diseaseName in ascending order
        }
    ]
    
    result = disease_ass1.aggregate(pipeline)
    df = pd.DataFrame(list(result))
    last_col = df.pop(df.columns[-1])  # remove the last column from the DataFrame
    df.insert(0, last_col.name, last_col)
    return df 


def agg_GennumClass():
      pipeline = [
          {
              '$group': {
                  '_id': '$diseaseClass',  # group by diseaseName field
                  'Number of Genes': {'$sum': '$NofGenes'}  # add geneSymbols to a set
              }
          },{
          '$project': {
              'Disease Class': '$_id',  # rename _id field to grouping_criteria
               # include the total field
          "_id":0, 'Number of Genes': 1
          }},
          {
              '$sort': {'Number of Genes': 1}  # sort by diseaseName in ascending order
          }
      ]
      
      result = disease_ass1.aggregate(pipeline)
      df = pd.DataFrame(list(result))
      last_col = df.pop(df.columns[-1])  # remove the last column from the DataFrame
      df.insert(0, last_col.name, last_col)
      return df      

def agg_gene1():
    pipeline = [
    {    
        '$group': {
            '_id': '$protein_class',  # group by diseaseName field
            'total Number of Diseases': {'$sum': '$NofDiseases'}  # add geneSymbols to a set
        }
    },{
    '$project': {
            'Protein Class': '$_id',  # rename _id field to grouping_criteria
             # include the total field
        "_id":0, 'total Number of Diseases': 1
        }},
    {
        
        '$sort': {'total Number of Diseases': 1}  # sort by diseaseName in ascending order
    }
]

    result = gene_ass1.aggregate(pipeline)
    df = pd.DataFrame(list(result))
    last_col = df.pop(df.columns[-1])  # remove the last column from the DataFrame
    df.insert(0, last_col.name, last_col)
    return df  


def mapreduce_dis():
    pipeline = [
        {
            '$project': {
                '_id': 0,
                'diseaseName': 1
            }
        },
        {
            '$unwind': '$diseaseName'
        },
        {
            '$project': {
                'words': {
                    '$filter': {
                        'input': {'$split': [{'$trim': {'input': '$diseaseName'}}, ' ']},
                        'cond': {'$ne': ['$$this', '']}
                    }
                }
            }},{
        '$group': {
            '_id': '$words',
            'count': {'$sum': 1}
        }
    },
    {
        '$sort': {'count': -1}
    }
    ]
    
    # execute the pipeline and print the results
    r=disease_ass1.aggregate(pipeline)
    df = pd.DataFrame(list(r))
    return df  

def mapreduce_combo():
    pipeline = [
    {
        '$project': {
            '_id': 0,
            'STITCH 1': 1
        }
    },
    {
        '$unwind': '$STITCH 1'
    },
    {
        '$project': {
            'words': {
                '$filter': {
                    'input': {'$split': [{'$trim': {'input': '$STITCH 1'}}, ' ']},
                    'cond': {'$ne': ['$$this', '']}
                }
            }
        }},{
    '$group': {
        '_id': '$words',
        'count': {'$sum': 1}
    }
},
{
    '$sort': {'count': -1}
}
]

# execute the pipeline and print the results
    r=bio_decagon_combo1.aggregate(pipeline)
    df = pd.DataFrame(list(r))
    return df
#####################################Random Query########
def Find_Disease(query):
    table=query.split(".")[0]
    qu=query.split(".")[1]
    qu1=qu.split("(")[0]
    table1=query.split("(")[1]
    table2=table1.split(")")[0]
    query_dict = json.loads(table2)
    r=disease_ass1.find(query_dict)
    df = pd.DataFrame(list(r))
    return df

def Delete_Disease(query):
    table=query.split(".")[0]
    qu=query.split(".")[1]
    qu1=qu.split("(")[0]    
    table1=query.split("(")[1]
    table2=table1.split(")")[0]
    query_dict = json.loads(table2)
    documents= disease_ass1.find_one(query_dict)
    if(documents!=None):
        d=disease_ass1.delete_many(query_dict)
        if (d.acknowledged==True):
            return 1
        else:
            return 0
    else:
        return 91

def Insert_Combo_Rand(query):
    table=query.split(".")[0]
    qu=query.split(".")[1]
    qu1=qu.split("(")[0]   
    table1=query.split("(")[1]
    table2=table1.split(")")[0]
    query_dict = json.loads(table2)
    
    d=bio_decagon_combo1.insert_one(query_dict)   
    if (d.acknowledged==True):
         return 1
    else:
         return 0
     
def Delete_Combo_Rand(query):
    table=query.split(".")[0]
    qu=query.split(".")[1]
    qu1=qu.split("(")[0]
    table1=query.split("(")[1]
    table2=table1.split(")")[0]
    query_dict = json.loads(table2)
    documents= bio_decagon_combo1.find_one(query_dict)
    if(documents!=None):
        d=bio_decagon_combo1.delete_many(query_dict)
        if (d.acknowledged==True):
            return 1
        else:
            return 0
    else:
        return 91

def Delete_gene_Rand(query):  
    table=query.split(".")[0]
    qu=query.split(".")[1]
    qu1=qu.split("(")[0]
    table1=query.split("(")[1]
    table2=table1.split(")")[0]
    query_dict = json.loads(table2)
    documents= gene_ass1.find_one(query_dict)
    if(documents!=None):
        d=gene_ass1.delete_many(query_dict)
        if (d.acknowledged==True):
            return 1
        else:
            return 0
    else:
        return 91


def Update_gene_Rand(query):
    table=query.split(".")[0]
    qu=query.split(".")[1]
    qu1=qu.split("(")[0]
    table1=query.split("(")[1]
    table2=table1.split(",")[0]
    table3=table1.split(",")[1]
    table4=table3.split(")")[0]
    query_dict = json.loads(table2)
    update_dict = json.loads(table4)
    d=gene_ass1.update_one(query_dict,update_dict)
    if (d.acknowledged==True):
            return 1
    else:
            return 0
#######################Indexing###########
def Index(index_fields,index_sorts):
    index_fields = [field.strip() for field in index_fields.split(',')]
    
    # Get the index sort orders from the user
    index_sorts = [int(sort.strip()) for sort in index_sorts.split(',')]
    
    # Create an index on the specified fields and sort orders
    index_spec = [(field, sort) for field, sort in zip(index_fields, index_sorts)]
    if (gene_ass1.create_index(index_spec)): 
       return 1
    else:
       return 0     

def Index2(index_fields,index_sorts):
     index_fields = [field.strip() for field in index_fields.split(',')]     
     # Get the index sort orders from the user
     index_sorts = [int(sort.strip()) for sort in index_sorts.split(',')]     
     # Create an index on the specified fields and sort orders
     index_spec = [(field, sort) for field, sort in zip(index_fields, index_sorts)]
     if(disease_ass1.create_index(index_spec)):
         return 1
     else:
         return 0
      
    
def Index3(index_fields,index_sorts):
     index_fields = [field.strip() for field in index_fields.split(',')]     
     # Get the index sort orders from the user
     index_sorts = [int(sort.strip()) for sort in index_sorts.split(',')]     
     # Create an index on the specified fields and sort orders
     index_spec = [(field, sort) for field, sort in zip(index_fields, index_sorts)]
     if (bio_decagon_combo1.create_index(index_spec)):
        return 1
     else:
        return 0
################################################################

def main():
    
    if selected == "Intro":
        #image = Image.open('im.png')
        col1,col2,col3=st.columns([1,3,1])
        with col2:
            st.image("im.png")
        st.markdown("<h6 style='text-align: center; color: white;'>The use of multiple drugs, termed polypharmacy, is common to treat patients with complex diseases or co-existing medical conditions. However, a major consequence of polypharmacy is a much higher risk of adverse side effects for the patient. Polypharmacy side effects emerge because of drug-drug interactions, in which activity of one drug may change, favorably or unfavorably, if taken with another drug. The approach constructs a multimodal graph of protein-protein interactions, drug-protein target interactions, and the polypharmacy side effects, which are represented as drug-drug interactions, where each side effect is an edge of a different type.</h6>", unsafe_allow_html=True)

    elif selected == "Find Queries":
        # Get a list of collection names in the database
        collection_names = ['bio_decagon_combo','bio_decagon_effectcategories','disease_associations','gene_associations']
        
        # Display a dropdown list of collection names
        selected_collection = st.selectbox("Select a collection", collection_names)
        if selected_collection:
            if(selected_collection=='bio_decagon_combo'):
                st.markdown('<h1 class="title">Search Bio Decagon Combo Collection to Find Side Effect Related Data</h1>', unsafe_allow_html=True)
                st.markdown('<p class="description">Enter a Side Effect Name to search in the collection:</p>', unsafe_allow_html=True)
                       # Define the sidebar with the tab options
                query = st.text_input('Side Effect Name', '', key='text-input')
                if st.button('Search'):
                        # Search for the text query in MongoDB
                        results = search_Side_Effect_Name_combo(query)
                        # Display the results in a DataFrame
                        if len(results) > 0:
                            st.markdown('<p class="description">Search Results:</p>', unsafe_allow_html=True)
                            st.table(results.style.set_table_attributes('class="result-table"'))
                        else:
                            st.warning('No results found.')
            elif(selected_collection=='bio_decagon_effectcategories'):
                    st.markdown('<h1 class="title">Search Bio Decagon Effect Categories Collection to Find Side Effect Related Data</h1>', unsafe_allow_html=True)
                    st.markdown('<p class="description">Enter a Side Effect Name to search in the collection:</p>', unsafe_allow_html=True)
                           # Define the sidebar with the tab options
                    query = st.text_input('Side Effect Name', '', key='text-input')
                    if st.button('Search'):
                            # Search for the text query in MongoDB
                            results = search_Side_Effect_Name_cattegory_First_One(query)
                            # Display the results in a DataFrame
                            if len(results) > 0:
                                st.markdown('<p class="description">Search Results:</p>', unsafe_allow_html=True)
                                st.table(results.style.set_table_attributes('class="result-table"'))
                            else:
                                st.warning('No results found.')
              
            elif(selected_collection=='disease_associations'):
                    st.markdown('<h1 class="title">Search Disease Associations Collection to Find Side Effect Related Disease Data</h1>', unsafe_allow_html=True)
                    st.markdown('<p class="description">Enter a Side Effect ID to search in the collection:</p>', unsafe_allow_html=True)
                           # Define the sidebar with the tab options
                    query = st.text_input('Side Effect ID', '', key='text-input')
                    if st.button('Search Based on ID'):
                            # Search for the text query in MongoDB
                            results = Side_Effect_Related_Disease_Data(query)
                            # Display the results in a DataFrame
                            if len(results) > 0:
                                st.markdown('<p class="description">Search Results:</p>', unsafe_allow_html=True)
                                st.table(results.style.set_table_attributes('class="result-table"'))
                            else:
                                st.warning('No results found.') 

                                
            elif(selected_collection=='gene_associations'):
                    st.markdown('<h1 class="title">Search Gene Associations Collection to Gene Related Data</h1>', unsafe_allow_html=True)
                    st.markdown('<p class="description">Enter a GeneID to search in the collection:</p>', unsafe_allow_html=True)
                           # Define the sidebar with the tab options
                    query = st.text_input('Gene ID', '', key='text-input')
                    if st.button('Search'):
                            # Search for the text query in MongoDB
                            results = Find_Gene_Associations_Data(query)
                            # Display the results in a DataFrame
                            if len(results) > 0:
                                st.markdown('<p class="description">Search Results:</p>', unsafe_allow_html=True)
                                st.table(results.style.set_table_attributes('class="result-table"'))
                            else:
                                st.warning('No results found.') 
                                
                                
                                
#########Insert#########  
    elif selected == "Insert Queries":
            collection_names = ['bio_decagon_combo','bio_decagon_effectcategories','disease_associations','gene_associations','bio_decagon_targets_all','bio_decagon_ppi','bio_decagon_targets','bio_decagon_mono']
           # Display a dropdown list of collection names
            selected_collection = st.selectbox("Select a collection", collection_names)
            if selected_collection:
                if(selected_collection=='bio_decagon_ppi'):
                    st.markdown('<h1 class="title">Insert One record into Bio Decagon PPI Collection </h1>', unsafe_allow_html=True)
                    st.markdown('<p class="description">Enter data to be inserted in the collection:</p>', unsafe_allow_html=True)
                           # Define the sidebar with the tab options
                    query1 = st.text_input('Gene 1', '', key='text-input1')
                    query2 = st.text_input('Gene 2', '', key='text-input2')
                    if st.button('Insert'):
                            # Search for the text query in MongoDB
                            results = Insert_PPI(query1,query2)
                            # Display the results in a DataFrame
                            if results > 0:
                                st.markdown('<p class="description">Inserted Successfully </p>', unsafe_allow_html=True)
                            else:
                                st.warning('Something Error in Inserting')
            
                elif(selected_collection=='bio_decagon_combo'):
                    st.markdown('<h1 class="title">Insert One record into Bio Decagon Combo Collection </h1>', unsafe_allow_html=True)
                    st.markdown('<p class="description">Enter data to be inserted in the collection:</p>', unsafe_allow_html=True)
                           # Define the sidebar with the tab options
                    query1 = st.text_input('STITCH 1', '', key='text-input1')
                    query2 = st.text_input('STITCH 2', '', key='text-input2')
                    query3 = st.text_input('Polypharmacy Side Effect ID', '', key='text-input3')
                    query4 = st.text_input('Side Effect Name', '', key='text-input4')
                    if st.button('Insert'):
                            # Search for the text query in MongoDB
                            results =  Inser_Combo(query1,query2,query3,query4)
                            # Display the results in a DataFrame
                            if results > 0:
                                st.markdown('<p class="description">Inserted Successfully </p>', unsafe_allow_html=True)
                            else:
                                st.warning('Something Error in Inserting')
                elif(selected_collection=='bio_decagon_effectcategories'):
                     st.markdown('<h1 class="title">Insert One record into Bio Decagon Effect Category Collection </h1>', unsafe_allow_html=True)
                     st.markdown('<p class="description">Enter data to be inserted in the collection:</p>', unsafe_allow_html=True)
                            # Define the sidebar with the tab options
                     query1 = st.text_input('Side Effect ID', '', key='text-input1')
                     query2 = st.text_input('Side Effect Name', '', key='text-input2')
                     query3 = st.text_input('Disease Class', '', key='text-input3')
                     if st.button('Insert'):
                             # Search for the text query in MongoDB
                             results =  Insert_Effect(query1,query2,query3)
                             # Display the results in a DataFrame
                             if results > 0:
                                 st.markdown('<p class="description">Inserted Successfully </p>', unsafe_allow_html=True)
                             else:
                                 st.warning('Something Error in Inserting')

                elif(selected_collection=='bio_decagon_mono'):
                     st.markdown('<h1 class="title">Insert One record into Bio Decagon Mono Collection </h1>', unsafe_allow_html=True)
                     st.markdown('<p class="description">Enter data to be inserted in the collection:</p>', unsafe_allow_html=True)
                            # Define the sidebar with the tab options
                     query1 = st.text_input('STITCH ID', '', key='text-input1')
                     query2 = st.text_input('Side Effect ID', '', key='text-input2')
                     query3= st.text_input('Side Effect Name', '', key='text-input3')
                     if st.button('Insert'):
                             # Search for the text query in MongoDB
                             results =  Insert_Mono(query1,query2,query3)
                             # Display the results in a DataFrame
                             if results > 0:
                                 st.markdown('<p class="description">Inserted Successfully </p>', unsafe_allow_html=True)
                             else:
                                 st.warning('Something Error in Inserting')

                elif(selected_collection=='bio_decagon_targets'):
                     st.markdown('<h1 class="title">Insert One record into Bio Decagon Targets Collection </h1>', unsafe_allow_html=True)
                     st.markdown('<p class="description">Enter data to be inserted in the collection:</p>', unsafe_allow_html=True)
                            # Define the sidebar with the tab options
                     query1 = st.text_input('STITCH ID', '', key='text-input1')
                     query2 = st.text_input('GENE ID', '', key='text-input2')
                     if st.button('Insert'):
                             # Search for the text query in MongoDB
                             results =  Insert_Target(query1,query2)
                             # Display the results in a DataFrame
                             if results > 0:
                                 st.markdown('<p class="description">Inserted Successfully </p>', unsafe_allow_html=True)
                             else:
                                 st.warning('Something Error in Inserting')
                
                elif(selected_collection=='bio_decagon_targets_all'):
                     st.markdown('<h1 class="title">Insert One record into Bio Decagon Targets All Collection </h1>', unsafe_allow_html=True)
                     st.markdown('<p class="description">Enter data to be inserted in the collection:</p>', unsafe_allow_html=True)
                            # Define the sidebar with the tab options
                     query1 = st.text_input('STITCH ID', '', key='text-input1')
                     query2 = st.text_input('GENE ID', '', key='text-input2')
                     if st.button('Insert'):
                             # Search for the text query in MongoDB
                             results =  Insert_Target_All(query1,query2)
                             # Display the results in a DataFrame
                             if results > 0:
                                 st.markdown('<p class="description">Inserted Successfully </p>', unsafe_allow_html=True)
                             else:
                                 st.warning('Something Error in Inserting')

                elif(selected_collection=='gene_associations'):
                     st.markdown('<h1 class="title">Insert One record into Gene Associations Collection </h1>', unsafe_allow_html=True)
                     st.markdown('<p class="description">Enter data to be inserted in the collection:</p>', unsafe_allow_html=True)
                            # Define the sidebar with the tab options
                     query1 = st.text_input('GENE ID', '', key='text-input1')
                     query2 = st.text_input('GENE Symbol', '', key='text-input2')
                     query3 = st.text_input('Protein Class Name', '', key='text-input3')

                     if st.button('Insert'):
                             # Search for the text query in MongoDB
                             results =  Insert_Gene_Associations(query1,query2,query3)
                             # Display the results in a DataFrame
                             if results > 0:
                                 st.markdown('<p class="description">Inserted Successfully </p>', unsafe_allow_html=True)
                             else:
                                 st.warning('Something Error in Inserting')
                elif(selected_collection=='disease_associations'):
                     st.markdown('<h1 class="title">Insert One record into Disease Associations Collection </h1>', unsafe_allow_html=True)
                     st.markdown('<p class="description">Enter data to be inserted in the collection:</p>', unsafe_allow_html=True)
                            # Define the sidebar with the tab options
                     query1 = st.text_input('Disease ID', '', key='text-input1')
                     query2 = st.text_input('Disease Name', '', key='text-input2')
                     query3 = st.text_input('Disease Type', '', key='text-input3')

                     if st.button('Insert'):
                             # Search for the text query in MongoDB
                             results =  Insert_Disease_Associations(query1,query2,query3)
                             # Display the results in a DataFrame
                             if results > 0:
                                 st.markdown('<p class="description">Inserted Successfully </p>', unsafe_allow_html=True)
                             else:
                                 st.warning('Something Error in Inserting')
                                                                  
#########Update#########                                
    elif selected == "Update Queries":
            collection_names = ['bio_decagon_effectcategories','gene_associations','bio_decagon_ppi','bio_decagon_targets']
           # Display a dropdown list of collection names
            selected_collection = st.selectbox("Select a collection", collection_names)
            if selected_collection:
                if(selected_collection=='bio_decagon_ppi'):
                    st.markdown('<h1 class="title">Update One record into Bio Decagon PPI Collection </h1>', unsafe_allow_html=True)
                    st.markdown('<p class="description">Enter data to be updated in the collection:</p>', unsafe_allow_html=True)
                           # Define the sidebar with the tab options
                    query1 = st.text_input('Gene 1', '', key='text-input1')
                    if(query1 !=""):
                        query2 = st.text_input('Gene 2', '', key='text-input2')
                        if st.button('Update'):
                                # Search for the text query in MongoDB
                                results = Update_PPI(query1,query2)
                                # Display the results in a DataFrame
                                if results > 0:
                                    st.markdown('<p class="description">Updated Successfully </p>', unsafe_allow_html=True)
                                else:
                                    st.warning('Something Error in Updating')
            

                elif(selected_collection=='bio_decagon_effectcategories'):
                     st.markdown('<h1 class="title">Update One record into Bio Decagon Effect Category Collection </h1>', unsafe_allow_html=True)
                     st.markdown('<p class="description">Enter data to be updated in the collection:</p>', unsafe_allow_html=True)
                            # Define the sidebar with the tab options
                     query1 = st.text_input('OLD Disease Class', '', key='text-input1')
                     if(query1 !=""):
                         query2 = st.text_input('NEW Disease Class', '', key='text-input2')
                         if st.button('Update'):
                                 # Search for the text query in MongoDB
                                 results = Update_Effect(query1,query2)
                                 # Display the results in a DataFrame
                                 if results > 0:
                                     st.markdown('<p class="description">Updated Successfully </p>', unsafe_allow_html=True)
                                 else:
                                     st.warning('Something Error in Updating')


                elif(selected_collection=='gene_associations'):
                     st.markdown('<h1 class="title">Update One record into Gene Associantions Collection </h1>', unsafe_allow_html=True)
                     st.markdown('<p class="description">Enter data to be updated in the collection:</p>', unsafe_allow_html=True)
                            # Define the sidebar with the tab options
                     query1 = st.text_input('Gene ID', '', key='text-input1')
                     if(query1 !=""):
                         query2 = st.text_input('NEW Number of Diseases Related to it ', '', key='text-input2')
                         if st.button('Update'):
                                 # Search for the text query in MongoDB
                                 results =Update_Gene_Association(query1,query2)
                                 # Display the results in a DataFrame
                                 if results > 0:
                                     st.markdown('<p class="description">Updated Successfully </p>', unsafe_allow_html=True)
                                 else:
                                     st.warning('Something Error in Updating')
                                     
                elif(selected_collection=='bio_decagon_targets'):
                     st.markdown('<h1 class="title">Update One record into Bio Decagon Targets Collection </h1>', unsafe_allow_html=True)
                     st.markdown('<p class="description">Enter data to be updated in the collection:</p>', unsafe_allow_html=True)
                            # Define the sidebar with the tab options
                     query1 = st.text_input('STITCH ID', '', key='text-input1')
                     if(query1 !=""):
                         query2 = st.text_input('Gene ID ', '', key='text-input2')
                         if st.button('Update'):
                                 # Search for the text query in MongoDB
                                 results =Update_Target(query1,query2)
                                 # Display the results in a DataFrame
                                 if results > 0:
                                     st.markdown('<p class="description">Updated Successfully </p>', unsafe_allow_html=True)
                                 else:
                                     st.warning('Something Error in Updating')
                                                                    
#########Delete#########                                
    elif selected == "Delete Queries":
            collection_names = ['bio_decagon_combo','bio_decagon_effectcategories','disease_associations','gene_associations','bio_decagon_targets_all','bio_decagon_ppi','bio_decagon_targets','bio_decagon_mono']
           # Display a dropdown list of collection names
            selected_collection = st.selectbox("Select a collection", collection_names)
            if selected_collection:
                if(selected_collection=='bio_decagon_combo'):
                    st.markdown('<h1 class="title">Delete many records from Bio Decagon Combo Collection </h1>', unsafe_allow_html=True)
                    st.markdown('<p class="description">Enter data to be deleted from the collection:</p>', unsafe_allow_html=True)
                           # Define the sidebar with the tab options
                    query1 = st.text_input('STITCH 1', '', key='text-input1')
                    query2 = st.text_input('Polypharmacy Side Effect ID', '', key='text-input2')
                    if st.button('Delete Based on STITCH ID'):
                        documents= bio_decagon_combo1.find_one({"STITCH 1":query1})
                        if (documents!=None):        
                            results = Delete_Decagon(query1)
                            # Display the results in a DataFrame
                            if results > 0:
                                st.write('<p class="description">Deleted Successfully </p>', unsafe_allow_html=True)
                            else:
                                st.warning('Something Error in Deleting')                                                        
                        else:
                            st.warning("Please Enter Valid STITCH ID")
                    if st.button('Delete Based on Polypharmacy Side Effect ID'):
                        documents= bio_decagon_combo1.find_one({"Polypharmacy Side Effect":query2})
                        if (documents!=None):        
                            results = Delete_Decagon2(query2)
                            # Display the results in a DataFrame
                            if results > 0:
                                st.write('<p class="description">Deleted Successfully </p>', unsafe_allow_html=True)
                            else:
                                st.warning('Something Error in Deleting')                                                        
                        else:
                            st.warning("Please Enter Valid Polypharmacy Side Effect ID")
                    st.write("")
                    query3 = st.text_input('Polypharmacy Side Effect ID', '', key='text-input3')        
                    if st.button('Delete from Categories'):
                         documents= bio_decagon_combo1.find_one({"Polypharmacy Side Effect":query3})
                         dd=decagon_effect1.find_one({"Side Effect":query3})
                         if (documents!=None and dd!=None):        
                             results = Delete_Decagon_Effect_Bridge(query3)
                             # Display the results in a DataFrame
                             if results > 0:
                                 st.write('<p class="description">Deleted Successfully </p>', unsafe_allow_html=True)
                             else:
                                 st.warning('Something Error in Deleting')                                                        
                         else:
                             st.warning("Please Enter Valid Polypharmacy Side Effect ID")
                            
            if(selected_collection=='bio_decagon_effectcategories'):
                st.markdown('<h1 class="title">Delete one record from Bio Decagon Effect Categories Collection </h1>', unsafe_allow_html=True)
                st.markdown('<p class="description">Enter data to be deleted from the collection:</p>', unsafe_allow_html=True)
                       # Define the sidebar with the tab options
                query2 = st.text_input('Side Effect Name', '', key='text-input2')
                if st.button('Delete'):
                    documents= decagon_effect1.find_one({"Side Effect Name":query2})
                    if (documents!=None):        
                        results = Delete_Decagon_Effect1(query2)
                        # Display the results in a DataFrame
                        if results > 0:
                            st.write('<p class="description">Deleted Successfully </p>', unsafe_allow_html=True)
                        else:
                            st.warning('Something Error in Deleting')                                                        
                    else:
                        st.warning("Please Enter Valid SIDE EFFECT NAME")
            
            if(selected_collection=='bio_decagon_mono'):
                st.markdown('<h1 class="title">Delete many records from Bio Decagon Mono Collection </h1>', unsafe_allow_html=True)
                st.markdown('<p class="description">Enter data to be deleted from the collection:</p>', unsafe_allow_html=True)
                       # Define the sidebar with the tab options
                query2 = st.text_input('STITCH ID', '', key='text-input2')
                if st.button('Delete'):
                    documents= decagon_mono1.find_one({"STITCH":query2})
                    if (documents!=None):        
                        results = Delete_Decagon_Mono1(query2)
                        # Display the results in a DataFrame
                        if results > 0:
                            st.write('<p class="description">Deleted Successfully </p>', unsafe_allow_html=True)
                        else:
                            st.warning('Something Error in Deleting')                                                        
                    else:
                        st.warning("Please Enter Valid STITCH ID")  
            if(selected_collection=='bio_decagon_ppi'):
                st.markdown('<h1 class="title">Delete many records from Bio Decagon PPI Collection </h1>', unsafe_allow_html=True)
                st.markdown('<p class="description">Enter data to be deleted from the collection:</p>', unsafe_allow_html=True)
                       # Define the sidebar with the tab options
                query2 = st.text_input('GENE 1 ID', '', key='text-input2')
                if st.button('Delete'):
                    documents= decagon_ppi1.find_one({"Gene 1":int(query2)})
                    if (documents!=None):        
                        results = Delete_Decagon_ppi1(query2)
                        # Display the results in a DataFrame
                        if results > 0:
                            st.write('<p class="description">Deleted Successfully </p>', unsafe_allow_html=True)
                        else:
                            st.warning('Something Error in Deleting')                                                        
                    else:
                        st.warning("Please Enter Valid GENE ID")             
            if(selected_collection=='bio_decagon_targets'):
                  st.markdown('<h1 class="title">Delete many records from Bio Decagon Targets Collection </h1>', unsafe_allow_html=True)
                  st.markdown('<p class="description">Enter data to be deleted from the collection:</p>', unsafe_allow_html=True)
                         # Define the sidebar with the tab options
                  query2 = st.text_input('STITCH ID', '', key='text-input2')
                  if st.button('Delete'):
                      documents= targets1.find_one({"STITCH":query2})
                      if (documents!=None):        
                          results = Delete_Target(query2)
                          # Display the results in a DataFrame
                          if results > 0:
                              st.write('<p class="description">Deleted Successfully </p>', unsafe_allow_html=True)
                          else:
                              st.warning('Something Error in Deleting')                                                        
                      else:
                          st.warning("Please Enter Valid STITCH ID")     
                          
            if(selected_collection=='bio_decagon_targets_all'):
                   st.markdown('<h1 class="title">Delete many records from Bio Decagon Targets All Collection </h1>', unsafe_allow_html=True)
                   st.markdown('<p class="description">Enter data to be deleted from the collection:</p>', unsafe_allow_html=True)
                          # Define the sidebar with the tab options
                   query2 = st.text_input('GENE ID', '', key='text-input2')
                   if st.button('Delete'):
                       documents= targetsall1.find_one({"Gene":int(query2)})
                       if (documents!=None):        
                           results = Delete_Targetsall1(query2)
                           # Display the results in a DataFrame
                           if results > 0:
                               st.write('<p class="description">Deleted Successfully </p>', unsafe_allow_html=True)
                           else:
                               st.warning('Something Error in Deleting')                                                        
                       else:
                           st.warning("Please Enter Valid GENE ID")  
                           
            if(selected_collection=='disease_associations'):
                   st.markdown('<h1 class="title">Delete many records from Disease Associations Collection </h1>', unsafe_allow_html=True)
                   st.markdown('<p class="description">Enter data to be deleted from the collection:</p>', unsafe_allow_html=True)
                          # Define the sidebar with the tab options
                   query1 = st.text_input('Disease Name', '', key='text-input1')
                   query2 = st.text_input('Disease Semantic Type', '', key='text-input2')
                   query3 = st.text_input('Disease Class', '', key='text-input3')

                   if st.button('Delete Based on Disease Name'):
                       documents= disease_ass1.find_one({"diseaseName":query1})
                       if (documents!=None):        
                           results = Delete_Disease_ass1(query1)
                           # Display the results in a DataFrame
                           if results > 0:
                               st.write('<p class="description">Deleted Successfully </p>', unsafe_allow_html=True)
                           else:
                               st.warning('Something Error in Deleting')                                                        
                       else:
                           st.warning("Please Enter Valid Disease Name")
                   if st.button('Delete Based on Disease Semantic Type'):
                       documents= disease_ass1.find_one({"diseaseSemanticType":query2})
                       if (documents!=None):        
                           results = Delete_Disease_ass2(query2)
                           # Display the results in a DataFrame
                           if results > 0:
                               st.write('<p class="description">Deleted Successfully </p>', unsafe_allow_html=True)
                           else:
                               st.warning('Something Error in Deleting')                                                        
                       else:
                           st.warning("Please Enter Valid Semantic Type")
                   if st.button('Delete Based on Disease Class'):
                       documents= disease_ass1.find_one({"diseaseClass":query3})
                       if (documents!=None):        
                           results = Delete_Disease_ass3(query3)
                           # Display the results in a DataFrame
                           if results > 0:
                               st.write('<p class="description">Deleted Successfully </p>', unsafe_allow_html=True)
                           else:
                               st.warning('Something Error in Deleting')                                                        
                       else:
                           st.warning("Please Enter Valid Disease Class") 
                           
            if(selected_collection=='gene_associations'):
                   st.markdown('<h1 class="title">Delete many records from Gene Associations Collection </h1>', unsafe_allow_html=True)
                   st.markdown('<p class="description">Enter data to be deleted from the collection:</p>', unsafe_allow_html=True)
                          # Define the sidebar with the tab options
                   query1 = st.text_input('Protein Class Name', '', key='text-input1')

                   if st.button('Delete'):
                       documents= gene_ass1.find_one({"protein_class_name":query1})
                       if (documents!=None):        
                           results = Delete_Gene_ass1(query1)
                           # Display the results in a DataFrame
                           if results > 0:
                               st.write('<p class="description">Deleted Successfully </p>', unsafe_allow_html=True)
                           else:
                               st.warning('Something Error in Deleting')                           
                       else:
                            st.warning("Please Enter Valid Protein Class") 
############################Aggregations####################################

                            
    elif selected == "Aggregations Queries":
                collection_names = ['bio_decagon_combo','disease_associations','gene_associations','bio_decagon_mono']
               # Display a dropdown list of collection names
                selected_collection = st.selectbox("Select a collection", collection_names)
                if selected_collection:
                    if(selected_collection=='bio_decagon_mono'):
                        st.markdown('<h1 class="title">Aggregation on Bio decagon mono collection </h1>', unsafe_allow_html=True)
                        st.markdown('<p class="description">Count number of side effescts related to STITCH ID</p>', unsafe_allow_html=True)
                        if st.button('Display'):
                               results = agg_mono()
                               # Display the results in a DataFrame
                               if len(results) > 0:
                                   st.markdown('<p class="description">Search Results:</p>', unsafe_allow_html=True)
                                   st.table(results.style.set_table_attributes('class="result-table"'))
                               else:
                                   st.warning('No results found.') 
                    elif(selected_collection=='disease_associations'):
                         st.markdown('<h1 class="title">Aggregation on Disease Associations collection </h1>', unsafe_allow_html=True)
                         if st.button('Disease Semantic Type Based on Disease Type'):
                                results = agg_disType()
                                # Display the results in a DataFrame
                                if len(results) > 0:
                                    st.markdown('<p class="description">Search Results:</p>', unsafe_allow_html=True)
                                    st.table(results.style.set_table_attributes('class="result-table"'))
                                else:
                                    st.warning('No results found.') 
                         elif st.button('Disease Semantic Type Based on Disease Class'):
                                results = agg_disClass()
                                # Display the results in a DataFrame
                                if len(results) > 0:
                                    st.markdown('<p class="description">Search Results:</p>', unsafe_allow_html=True)
                                    st.table(results.style.set_table_attributes('class="result-table"'))
                                else:
                                    st.warning('No results found.')   
                         elif st.button('Gene Numbers Based on Disease Type'):
                                results = agg_Gennum()
                                # Display the results in a DataFrame
                                if len(results) > 0:
                                    st.markdown('<p class="description">Search Results:</p>', unsafe_allow_html=True)
                                    st.table(results.style.set_table_attributes('class="result-table"'))
                                else:
                                    st.warning('No results found.')          
                         elif st.button('Gene Numbers Based on Disease Class'):
                              results = agg_GennumClass()
                              # Display the results in a DataFrame
                              if len(results) > 0:
                                  st.markdown('<p class="description">Search Results:</p>', unsafe_allow_html=True)
                                  st.table(results.style.set_table_attributes('class="result-table"'))
                              else:
                                  st.warning('No results found.')
                         elif st.button('Map Reduce Based on disease name'):
                               results = mapreduce_dis()
                               # Display the results in a DataFrame
                               if len(results) > 0:
                                   st.markdown('<p class="description">Search Results:</p>', unsafe_allow_html=True)
                                   st.table(results.style.set_table_attributes('class="result-table"'))
                               else:
                                   st.warning('No results found.')        
                                  
                    elif(selected_collection=='gene_associations'):
                             st.markdown('<h1 class="title">Aggregation on Gene Associations collection </h1>', unsafe_allow_html=True)
                             if st.button('Display'):
                                    results = agg_gene1()
                                    # Display the results in a DataFrame
                                    if len(results) > 0:
                                        st.markdown('<p class="description">Search Results:</p>', unsafe_allow_html=True)
                                        st.table(results.style.set_table_attributes('class="result-table"'))
                                    else:
                                        st.warning('No results found.')
                    elif(selected_collection=='bio_decagon_combo'):
                        st.markdown('<h1 class="title">Aggregation on Bio decagon combo collection </h1>', unsafe_allow_html=True)
                        st.markdown('<p class="description">Count number of side effescts related to STITCH ID</p>', unsafe_allow_html=True)
                        if st.button('Display'):
                               results = mapreduce_combo()
                               # Display the results in a DataFrame
                               if len(results) > 0:
                                   st.markdown('<p class="description">Search Results:</p>', unsafe_allow_html=True)
                                   st.table(results.style.set_table_attributes('class="result-table"'))
                               else:
                                   st.warning('No results found.')                    

#########################RandomQuey##############
    elif selected == "Random Query":
                collection_names = ['disease_associations','bio_decagon_combo','gene_associations']
               # Display a dropdown list of collection names
                selected_collection = st.selectbox("Select a collection", collection_names)
                #select_query=['Find','Insert','Delete','Update']
                if selected_collection:
                    if(selected_collection=='disease_associations'):
                        select_query=['Find','Delete']
                        Select_Query = st.selectbox("Select a Query to Do", select_query)
                        if(Select_Query):
                            if(Select_Query=='Find'):
                                st.markdown('<h1 class="title">Enter your Query here </h1>', unsafe_allow_html=True)
                                query1 = st.text_input('Query Here', '', key='text-input1')
                                if st.button('Query'):
                                       results =Find_Disease(query1)
                                       # Display the results in a DataFrame
                                       if len(results) > 0:
                                           st.markdown('<p class="description">Search Results:</p>', unsafe_allow_html=True)
                                           st.table(results.style.set_table_attributes('class="result-table"'))
                                       else:
                                           st.warning('No results found.') 
                            elif(Select_Query=='Delete'):
                                st.markdown('<h1 class="title">Enter your Query here </h1>', unsafe_allow_html=True)
                                query1 = st.text_input('Query Here', '', key='text-input1')
                                if st.button('Query'):
                                       results =Delete_Disease(query1)
                                       # Display the results in a DataFrame
                                       if results == 1:
                                           st.write('<p class="description">Deleted Successfully </p>', unsafe_allow_html=True)
                                       elif results==91:
                                           st.warning('Enter Valid Query PLEASE.')
                                       else:
                                           st.warning('Something Error in Deleting')

                    elif(selected_collection=='bio_decagon_combo'):
                        select_query=['Insert','Delete']
                        Select_Query = st.selectbox("Select a Query to Do", select_query)
                        if(Select_Query):
                            if(Select_Query=='Insert'):
                                st.markdown('<h1 class="title">Enter your Query here </h1>', unsafe_allow_html=True)
                                query1 = st.text_input('Query Here', '', key='text-input1')
                                if st.button('Query'):
                                       results =Insert_Combo_Rand(query1)
                                       # Display the results in a DataFrame
                                       if results > 0:
                                           st.markdown('<p class="description">Inserted Successfully</p>', unsafe_allow_html=True)
                                       else:
                                           st.warning('Something Error in Inserting')
                            elif(Select_Query=='Delete'):
                                st.markdown('<h1 class="title">Enter your Query here </h1>', unsafe_allow_html=True)
                                query1 = st.text_input('Query Here', '', key='text-input1')
                                if st.button('Query'):
                                       results =Delete_Combo_Rand(query1)
                                       # Display the results in a DataFrame
                                       if results == 1:
                                           st.write('<p class="description">Deleted Successfully </p>', unsafe_allow_html=True)
                                       elif results==91:
                                           st.warning('Enter Valid Query PLEASE.')
                                       else:
                                           st.warning('Something Error in Deleting')
                    elif(selected_collection=='gene_associations'):
                        select_query=['Update','Delete']
                        Select_Query = st.selectbox("Select a Query to Do", select_query)
                        if(Select_Query):
                            if(Select_Query=='Update'):
                                st.markdown('<h1 class="title">Enter your Query here </h1>', unsafe_allow_html=True)
                                query1 = st.text_input('Query Here', '', key='text-input1')
                                if st.button('Query'):
                                       results =Update_gene_Rand(query1)
                                       # Display the results in a DataFrame
                                       if results == 1:
                                           st.write('<p class="description">Updating Successfully </p>', unsafe_allow_html=True)
                                       else:
                                           st.warning('Something Error in Updating')   
                            elif(Select_Query=='Delete'):
                                st.markdown('<h1 class="title">Enter your Query here </h1>', unsafe_allow_html=True)
                                query1 = st.text_input('Query Here', '', key='text-input1')
                                if st.button('Query'):
                                       results =Delete_gene_Rand(query1)
                                       # Display the results in a DataFrame
                                       if results == 1:
                                           st.write('<p class="description">Deleted Successfully </p>', unsafe_allow_html=True)
                                       elif results==91:
                                           st.warning('Enter Valid Query PLEASE.')
                                       else:
                                           st.warning('Something Error in Deleting')                       
                                           
    elif selected == "Indexing and hashing":
                collection_names = ['gene_associations','disease_associations','bio_decagon_combo']
               # Display a dropdown list of collection names
                selected_collection = st.selectbox("Select a collection", collection_names)
                if selected_collection:
                    if(selected_collection=='gene_associations'):
                        st.markdown('<h1 class="title">Indexing in the gene association collection </h1>', unsafe_allow_html=True)
                        st.markdown('<p class="description">Enter a list of index fields separated by commas:</p>', unsafe_allow_html=True)
                               # Define the sidebar with the tab options
                        index_fields = st.text_input('Index Fields', '', key='text-input1')
                        st.markdown('<p class="description">Enter a list of index sorts separated by commas:</p>', unsafe_allow_html=True)
                        index_sorts = st.text_input('Index Sorts', '', key='text-input2')
                        if st.button('Indexing'):
                                # Search for the text query in MongoDB
                                results = Index(index_fields,index_sorts)
                                # Display the results in a DataFrame
                                if results > 0:
                                    st.markdown('<p class="description">Indexed Successfully </p>', unsafe_allow_html=True)
                                else:
                                    st.warning('Something Error in Indexing')  
                    elif(selected_collection=='disease_associations'):
                        st.markdown('<h1 class="title">Indexing in the disease association collection </h1>', unsafe_allow_html=True)
                        st.markdown('<p class="description">Enter a list of index fields separated by commas:</p>', unsafe_allow_html=True)
                               # Define the sidebar with the tab options
                        index_fields = st.text_input('Index Fields', '', key='text-input1')
                        st.markdown('<p class="description">Enter a list of index sorts separated by commas:</p>', unsafe_allow_html=True)
                        index_sorts = st.text_input('Index Sorts', '', key='text-input2')
                        if st.button('Indexing'):
                                # Search for the text query in MongoDB
                                results = Index2(index_fields,index_sorts)
                                # Display the results in a DataFrame
                                if results > 0:
                                    st.markdown('<p class="description">Indexed Successfully </p>', unsafe_allow_html=True)
                                else:
                                    st.warning('Something Error in Indexing')
                                    
                    elif(selected_collection=='bio_decagon_combo'):
                         st.markdown('<h1 class="title">Indexing in the Bio decagon combo collection </h1>', unsafe_allow_html=True)
                         st.markdown('<p class="description">Enter a list of index fields separated by commas:</p>', unsafe_allow_html=True)
                                # Define the sidebar with the tab options
                         index_fields = st.text_input('Index Fields', '', key='text-input1')
                         st.markdown('<p class="description">Enter a list of index sorts separated by commas:</p>', unsafe_allow_html=True)
                         index_sorts = st.text_input('Index Sorts', '', key='text-input2')
                         if st.button('Indexing'):
                                 # Search for the text query in MongoDB
                                 results = Index3(index_fields,index_sorts)
                                 # Display the results in a DataFrame
                                 if results > 0:
                                     st.markdown('<p class="description">Indexed Successfully </p>', unsafe_allow_html=True)
                                 else:
                                     st.warning('Something Error in Indexing')                
                    
                        
###########################Plots##################################
    elif selected == "Plots On Data":
            st.markdown('<h3 class="title">Some Bar Plots to Realize the relations between data </h3>', unsafe_allow_html=True) 
            # Create two plots side-by-side
            col1, col2 = st.columns(2)
            col3, col4 = st.columns(2) 
              

            with col1:
                st.pyplot(figbar1)
            
            with col2:
                st.pyplot(figbar2)
            
            with col3:
                st.pyplot(figbar3)
            
            with col4:
                st.pyplot(figbar4)
            st.markdown('<h3 class="title">Pie Plots to Realize the relations between data </h3>', unsafe_allow_html=True) 
            col5, col6 = st.columns(2)
            with col5:
                 st.pyplot(figpie1)
             
            with col6:
                 st.pyplot(figpie2)
            st.markdown('<h3 class="title">Heat Maps Plot to Realize the correlation between data </h3>', unsafe_allow_html=True) 
            col7, col77 = st.columns(2)
            with col7:
                st.pyplot(figheat1)
                
            st.markdown('<h3 class="title">Violin Plots to Realize the distribution of numerical data </h3>', unsafe_allow_html=True) 
            col8, col9 = st.columns(2)
            with col8:
                 st.pyplot(figviol1)             
            with col9:
                 st.pyplot(figviol2)  

            
###############################Generated Plots#####################################################
#---> ######1

# Get the count of each unique value in a column
value_counts = combo['Polypharmacy Side Effect'].value_counts()

x=[]
y=[]
for k,v in zip(value_counts.index,value_counts.values):
    if(v>24000):
        x.append(k)
        y.append(v)

# Create a bar plot of the value counts
figbar1, ax1 = plt.subplots(figsize=(12, 10))
ax1.bar(x, y,width=0.5, linewidth=10,color="#B3C890")
plt.ylim(min(y)-500, max(y)+500)
# Set the title and axis labels
plt.title('Repetition of Drugs that cause side effect')
plt.xlabel('Drugs')
plt.ylabel('Count')

#---> ##########2

# Get the count of each unique value in a column
value_counts = combo['Side Effect Name'].value_counts()

x=[]
y=[]
for k,v in zip(value_counts.index,value_counts.values):
    if(v>24000):
        x.append(k)
        y.append(v)

# Create a bar plot of the value counts
figbar2, ax2 = plt.subplots(figsize=(12, 10))
ax2.bar(x, y,width=0.4, linewidth=8,color="#E8A0BF")
plt.ylim(min(y)-500, max(y)+500)
# Set the title and axis labels
plt.title('Repetition of Side Effect')
plt.xlabel('Side Effect Name')
plt.ylabel('Count of Repetition')

#---> ##########3

pairs = pd.DataFrame({'Pair': combo['STITCH 1'] + ' - ' + combo['STITCH 2']})

# count the occurrences of each pair
pair_counts = pairs.groupby('Pair').size().reset_index(name='Count')

pair_count_sorted= pair_counts.sort_values('Count',ascending=False)

# print the pairs and their counts

x=pair_count_sorted['Pair'][:5]
y=pair_count_sorted['Count'][:5]

# create a bar chart of the pairs and their counts
figbar3, ax3 = plt.subplots(figsize=(12,9))
#figbar3 = plt.figure()

ax3.bar(x, y,width=0.5, linewidth=8,color='#D4ADFC')
# add labels to the top of each bar
for i, v in enumerate(y):
    plt.text(i, v + 2.5, str(v), ha='center')
plt.xticks(rotation=90)
plt.xlabel('Drug Pairs')
plt.ylabel('Counts')
plt.title('The Most Five repeated pairs of STITCH 1 and STITCH 2')

#---> ##########4

#عدد كل جين وتكراره مع الstitch id

# Group the dataframe by each record's unique identifier and count the number of elements in each group
counts = targets.groupby('STITCH')['Gene'].count().value_counts()
# Create a new dataframe with the counts for each number of replicated elements
counts_df = pd.DataFrame({'replicated elements': counts.index, 'count': counts.values})
figbar4, ax4 = plt.subplots()
fig = plt.figure(figsize=(10, 9))
# Create a stacked bar chart of the counts
ax4.set_title('Counts of Records index with Replicated Elements')
# Add axis labels and a title
ax4.set_xlabel('Number of replicated elements')
ax4.set_ylabel('Count')
counts_df.plot(kind='bar', x='replicated elements', y='count', stacked=True, figsize=(13,11),ax=ax4)



#----> ###############5 


# Get the count of each unique value in a column
value_counts = combo['Side Effect Name'].value_counts()
x=[]
y=[]
for k,v in zip(value_counts.index,value_counts.values):
    if(v>24000):
        x.append(k)
        y.append(v)
colors = ['#E8A0BF', '#2B3467', '#BAD7E9', '#9E6F21', '#EB455F','#FF6969']
fig = plt.figure(figsize=(12, 12))
figpie1, ax5 = plt.subplots()
# Create a pie chart of the value counts
plt.title('Percentage of Disease Classes for Most Repeated Side Effect of Interacted Drugs')
ax5.pie(y, labels=x, autopct='%1.1f%%',colors=colors)

#----> ###############6



# Get the count of each unique value in a column
value_counts = combo['Side Effect Name'].value_counts()
x=[]
y=[]
d=[]
q=[]
for l,k,v in zip(combo['Polypharmacy Side Effect'],value_counts.index,value_counts.values):
    if(v>24000):
        x.append(k)
        y.append(v)
        for a,m in zip(list(set(disease_ass['diseaseId'])),list((disease_ass['diseaseSemanticType']))):
            if(l==a):
                q.append(a)
                d.append(m)
my_dict={}                
for k, v in zip(d,y):
    if k not in my_dict:
        my_dict[k] = v
    else:
        my_dict[k] += v
colors = [ '#106005', '#BAD7E9', '#EBD8B2', '#19A7CE','#FF6969']
fig = plt.figure(figsize=(12,12))
figpie2, ax6 = plt.subplots()
# Create a pie chart of the value counts
ax6.set_title('Percentage of Disease Semantic Type for Most Repeated Side Effect of Interacted Drugs')
ax6.pie(list(my_dict.values()), labels=list(my_dict.keys()), autopct='%1.1f%%',colors=colors)


#------>###########7

# Create a heatmap of the gene-disease associations in the gene data
fig = plt.figure(figsize=(12,12))
figheat1, ax7 = plt.subplots()
sns.heatmap(gene_ass.corr(), cmap='coolwarm')
ax7.set_title('Gene-Disease Associations Heatmap')



#------>#####8
# Load the data into pandas DataFrames
# Create a violin plot of the distribution of the 'Polymerase inhibitor' target class
fig = plt.figure(figsize=(12,12))
figviol1, ax8 = plt.subplots()
ax8=sns.violinplot(x='NofDiseases', data=gene_ass)
ax8.set_xlim(-10, 100)
ax8.set_ylim(-3, 5)
plt.title('Distribution of NofDiseases related to gene')




#------>######9

fig = plt.figure(figsize=(12,12))
figviol2, ax9 = plt.subplots()

# Create a violin plot of the distribution of the 'Polymerase inhibitor' target class
ax9=sns.violinplot(x='NofGenes', data=disease_ass)
ax9.set_xlim(-50, 200)
ax9.set_ylim(-3, 5)
plt.title('Distribution of NofGenes related to diseases')



#########################################################################################
col1, col2 = st.columns([1, 10])
with col1:
    st.image("logo2.png", width=100)

with col2:
    selected = option_menu(None, ["Intro","Find Queries","Insert Queries","Update Queries","Delete Queries","Aggregations Queries", 'Random Query','Indexing and hashing',"Plots On Data"], 
         icons=['house', 'cloud-upload', "list-task", 'gear'], 
         menu_icon="cast", default_index=0, orientation="horizontal",
         styles={
             "container": {"padding": "0!important", "background-color": "##FFFF00","display":"inline"},
             "icon": {"color": "orange", "font-size": "15px"}, 
             "nav-link": {"font-size": "15px", "text-align": "left", "margin":"10px", "--hover-color": "#blue"},
             "nav-link-selected": {"background-color": "red"},
         }
     )     
    
    


   
if __name__ == '__main__':
    main()
