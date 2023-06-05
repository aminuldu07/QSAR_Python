{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 4,
   "id": "b311016b-a6e3-40fb-bd8b-f909c5f4ebbb",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "C:\\Users\\mdaminulisla.prodhan\\All_My_Miscellenous\\pubchempy\n"
     ]
    }
   ],
   "source": [
    "# Get the current directory of the notebook file\n",
    "\n",
    "import os\n",
    "\n",
    "print(os.getcwd())\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "819dffb2",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Initial processing of the csv file (\"merged_on_Approval_ID.csv\") for getting unique INCHIKEY/SMILES\n",
    "# Deleting duplicate INCHIKEY from the \"merged_on_Approval_ID.csv\"\n",
    "# unique_inchikeys\n",
    "\n",
    "import pandas as pd\n",
    "\n",
    "# Read the CSV file \"merged_on_Approval_ID.csv\"\n",
    "df_merged = pd.read_csv('C:/Users/mdaminulisla.prodhan/All_My_Miscellenous/pubchempy/merged_on_Approval_ID.csv')\n",
    "\n",
    "# Drop duplicate rows based on the \"INCHIKEY\" column\n",
    "unique_df = df_merged.drop_duplicates(subset='INCHIKEY')\n",
    "\n",
    "# Save the unique dataframe to a new CSV file\n",
    "unique_df.to_csv('C:/Users/mdaminulisla.prodhan/All_My_Miscellenous/pubchempy/unique_inchikeys.csv', index=False)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "14125347",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "The files are identical.\n"
     ]
    }
   ],
   "source": [
    "# Checking the effectiveness of deleting duplicate INCHIKEY by agian deleting the duplicate SMILES values\n",
    "# and checking the differnce between these two files (two files should be identical)\n",
    "# unique_smiles\n",
    "\n",
    "# Read the CSV file \"unique_inchikeys.csv\"\n",
    "df_unique_inchikeys = pd.read_csv('C:/Users/mdaminulisla.prodhan/All_My_Miscellenous/pubchempy/unique_inchikeys.csv')\n",
    "\n",
    "# Drop duplicate rows based on the \"SMILES\" column\n",
    "unique_smiles_df = df_unique_inchikeys.drop_duplicates(subset='SMILES')\n",
    "\n",
    "# Save the unique SMILES dataframe to a new CSV file\n",
    "unique_smiles_df.to_csv('C:/Users/mdaminulisla.prodhan/All_My_Miscellenous/pubchempy/unique_smiles.csv', index=False)\n",
    "\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "e2d88623",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Determine the differnce between the \"unique_inchikeys.csv\" and \"unique_smiles.csv\"\n",
    "# Both file should be indentical\n",
    "\n",
    "def compare_csv_files(file1, file2):\n",
    "    df1 = pd.read_csv(file1)\n",
    "    df2 = pd.read_csv(file2)\n",
    "\n",
    "    # Making sure both DataFrames are sorted in the same way\n",
    "    df1 = df1.sort_values(by=df1.columns.tolist()).reset_index(drop=True)\n",
    "    df2 = df2.sort_values(by=df2.columns.tolist()).reset_index(drop=True)\n",
    "\n",
    "    # Checking if the two DataFrames are identical\n",
    "    are_identical = df1.equals(df2)\n",
    "    \n",
    "    return are_identical\n",
    "\n",
    "is_identical = compare_csv_files(\"unique_inchikeys.csv\", \"unique_smiles.csv\")\n",
    "if is_identical:\n",
    "    print(\"The files are identical.\")\n",
    "else:\n",
    "    print(\"The files are different.\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "id": "5d7953d0-a4e8-46fc-abfe-14e4ae27e46b",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Generating files containing finally selected SMILES from \"U_SMILES.csv\" and SMILES and \n",
    "# INCHIKEY from the \"unique_inchikeys.csv\"\n",
    "# SMILES = SMILES1\n",
    "\n",
    "import pandas as pd\n",
    "\n",
    "# Read the first CSV file \"U_SMILES.csv\"\n",
    "df_smiles = pd.read_csv('C:/Users/mdaminulisla.prodhan/All_My_Miscellenous/pubchempy/U_SMILES.csv')\n",
    "\n",
    "# Read the second CSV file \"merged_on_Approval_ID.csv\"\n",
    "df_unique_inchikeys = pd.read_csv('C:/Users/mdaminulisla.prodhan/All_My_Miscellenous/pubchempy/unique_inchikeys.csv')\n",
    "\n",
    "\n",
    "# Merge the two dataframes based on the condition SMILES = SMILES1\n",
    "merged_df = pd.merge(df_smiles, df_unique_inchikeys, how='inner', left_on='SMILES1', right_on='SMILES')\n",
    "\n",
    "# Select the desired columns\n",
    "result_df = merged_df[['SMILES1', 'SMILES', 'INCHIKEY']]\n",
    "\n",
    "# Save the result to a new CSV file\n",
    "result_df.to_csv('C:/Users/mdaminulisla.prodhan/All_My_Miscellenous/pubchempy/smile_smiles1_Inchikey.csv', index=False)\n",
    "\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "id": "653a0b32",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Convert the INCHIKEY to inchi string using pubchempy package \n",
    "\n",
    "import requests\n",
    "\n",
    "# Read the input CSV file\n",
    "df = pd.read_csv(r'C:\\Users\\mdaminulisla.prodhan\\All_My_Miscellenous\\pubchempy\\smile_smiles1_Inchikey.csv')\n",
    "\n",
    "# Create a new column for InChI\n",
    "df['InChI'] = ''\n",
    "\n",
    "# Iterate over the rows and retrieve InChI from PubChem using InChIKey\n",
    "for index, row in df.iterrows():\n",
    "    inchi_key = row['INCHIKEY']\n",
    "    try:\n",
    "        response = requests.get(f\"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/inchikey/{inchi_key}/property/InChI/txt\")\n",
    "        if response.status_code == 200:\n",
    "            inchi = response.text.strip()\n",
    "            df.at[index, 'InChI'] = inchi\n",
    "        else:\n",
    "            df.at[index, 'InChI'] = 'Error'\n",
    "    except:\n",
    "        df.at[index, 'InChI'] = 'Error'\n",
    "\n",
    "# Save the updated DataFrame to a new CSV file\n",
    "df.to_csv(r'C:\\Users\\mdaminulisla.prodhan\\All_My_Miscellenous\\pubchempy\\INCHIKEY_to_inchi.csv', index=False)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "a35308d6",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.9.13"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
