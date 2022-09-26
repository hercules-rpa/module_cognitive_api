from flask                                   import Blueprint, request, abort
from flask.wrappers                          import Response
from flask_restful                           import Api, Resource
from module_cognitive_treelogic.PDF2Table    import ProcessExtractTable
from module_cognitive_treelogic.ExtractXML   import ProcessExtractXml
from module_cognitive_treelogic.WebScrapping import WebScrapping
from module_cognitive_treelogic              import DataMining

import os
import json

pdf_to_table_v1_0_bp = Blueprint('pdf_to_table_v1_0_bp', __name__)
api = Api(pdf_to_table_v1_0_bp)

def getBlueprint():
    return pdf_to_table_v1_0_bp

class PDF2Table(Resource):
    def post(self):
        """
        Extrae tablas de imágenes o documentos PDF's  que te devuelve en un dataframe y adicionalmente, si se ha especificado, en un formato XLSX a través del correo electrónico.
        """
        solicitud_pdf = request.get_json(force=True)
        try:
            pdf = ProcessExtractTable(solicitud_pdf)
            result = pdf.execute()
            if len(result) > 0:
                return Response(result, status=200, mimetype='application/json')
            else:
                return Response(status=204)
        except Exception as e:
            abort(400, description=str(e))

class ExtractXMLExecute(Resource):
    def post(self):
        """
        Devuelve los nodos XML dado la URL y el fichero XML.
        """
        solicitud_xml = request.get_json(force=True)
        try:
            result = []
            xml = ProcessExtractXml(solicitud_xml)
            result = xml.execute()
            if result:
                return Response(result, status=200, mimetype='application/json')
            else:
                return Response(status=204)
        except Exception as e:
            abort(400, description=str(e))

class ExtractXMLGetDocument(Resource):
    def post(self):
        """
        Esta llamada consulta la url_origen dado y escribe el resultado, si existe, en el destino seleccionado. Devuelve el código de respuesta a la llamada con la url_origen.
        """
        solicitud_xml = request.get_json(force=True)
        try:
            xml = ProcessExtractXml(solicitud_xml)
            result = xml.traer_documento(solicitud_xml['origen'], solicitud_xml['destino'])
            if result != 404:
                return Response(result, status=200, mimetype='application/json')
            else:
                return Response(status=204)
        except Exception as e:
            abort(400, description=str(e))

class ExtractXMLGetDictionary(Resource):
    def post(self):
        """
        Dado un fichero XML y los parámetros devuelve un diccionario con el resultado de ese fichero XML.
        """
        solicitud_xml = request.get_json(force=True)
        try:
            result = {}
            xml = ProcessExtractXml(solicitud_xml)
            result = xml.obtener_diccionario(solicitud_xml['filename'], solicitud_xml['rootname'], solicitud_xml['atribname'], solicitud_xml['childsname'])
            print(result)
            if result:
                return Response(result, status=200, mimetype='application/json')
            else:
                return Response(status=204)
        except Exception as e:
            abort(400, description=str(e))

class WebScrappingBDNSSearch(Resource):
    def post(self):
        """
        Esta llamada consulta la página web de la Base de datos nacional de subvenciones y te devuelve el resultado en formato CSV de la consulta realizada con los parámetros dados.
        """
        solicitud_bdns = request.get_json(force=True)
        try:
            bdns = WebScrapping()
            try:
                args = solicitud_bdns['args']
                bdns.search_with_date_BDNS(solicitud_bdns['start_date'], solicitud_bdns['end_date'], args)
            except:
                bdns.search_with_date_BDNS(solicitud_bdns['start_date'], solicitud_bdns['end_date'])
                #esto debería subirse al CDN para descargarlo con el path que le dieramos.
            return Response(os.path.dirname(os.path.realpath(__file__))+"/convocatorias.csv", status=200, mimetype='application/json')
        except Exception as e:
            abort(400, description=str(e))

class WebScrappingBDNSData(Resource):
    def post(self):
        """
        Dado el número de la BDNS te devuelve la información ampliada en la página web sobre dicha convocatoria.
        """
        solicitud_bdns = request.get_json(force=True)
        try:
            result = {}
            bdns = WebScrapping()
            result = bdns.obtain_data_bdns(solicitud_bdns['bdns'])
            if result:
                return Response(json.dumps(result), status=200, mimetype='application/json')
            else:
                return Response(status=204)
        except Exception as e:
            abort(400, description=str(e))    

class DataMiningGetAllCluster(Resource):
    def get(self):
        """
        Devuelve todo el cluster de la llamada SPARQL que realiza al entorno EDMA con toda la información sobre investigadores.
        """
        try:
            result = {}
            DataMining.load_model()
            result = DataMining.get_all_cluster()
            if not result.empty:
                return Response(result.to_json(), status=200, mimetype='application/json')
            else:
                return Response(status=204)
        except Exception as e:
            abort(400, description=str(e))

class DataMiningGetAllCategories(Resource):
    def get(self):
        """
        Devuelve una lista de las categories extraídas del dataframe de la consulta SPARQL que se realiza al entorno EDMA.
        """
        try:
            result = {}
            DataMining.load_model()
            result = DataMining.get_all_categories()
            if result:
                return Response(json.dumps(result), status=200, mimetype='application/json')
            else:
                return Response(status=204)
        except Exception as e:
            abort(400, description=str(e))  

class DataMiningGetAllTag(Resource):
    def get(self):
        """
        Devuelve una lista de tags extraídos del dataframe de la consulta SPARQL que se realiza al entorno EDMA.
        """
        try:
            result = {}
            DataMining.load_model()
            result = DataMining.get_all_tag()
            if result:
                return Response(json.dumps(result), status=200, mimetype='application/json')
            else:
                return Response(status=204)
        except Exception as e:
            abort(400, description=str(e)) 

class DataMiningGetCategoriesInterestResearch(Resource):
    def post(self):
        """
        Devuelve una lista de categorías en las que el investigador ha participado.
        """
        solicitud_datamining = request.get_json(force=True)
        try:
            result = {}
            DataMining.load_model()
            result = DataMining.get_categories_interest_research(solicitud_datamining['email'])
            if result:
                return Response(json.dumps(result), status=200, mimetype='application/json')
            else:
                return Response(status=204)
        except Exception as e:
            abort(400, description=str(e))  

class DataMiningGetTagsInterestResearch(Resource):
    def post(self):
        """
        Devuelve una lista de tags en las que el investigado ha participado.
        """
        solicitud_datamining = request.get_json(force=True)
        try:
            result = {}
            DataMining.load_model()
            result = DataMining.get_tags_interest_research(solicitud_datamining['email'])
            if result:
                return Response(json.dumps(result), status=200, mimetype='application/json')
            else:
                return Response(status=204)
        except Exception as e:
            abort(400, description=str(e))  

class DataMiningGetResearchClusters(Resource):
    def post(self):
        """
        Devuelve una lista de clusters en las que el investigador ha participado.
        """
        solicitud_datamining = request.get_json(force=True)
        try:
            result = {}
            DataMining.load_model()
            result = DataMining.get_research_clusters(solicitud_datamining['email'])
            if result:
                return Response(json.dumps(result), status=200, mimetype='application/json')
            else:
                return Response(status=204)
        except Exception as e:
            abort(400, description=str(e))  

class DataMiningGetResearchRelation(Resource):
    def post(self):
        """
        Devuelve una lista de las relaciones que tiene el investigador.
        """
        solicitud_datamining = request.get_json(force=True)
        try:
            result = {}
            DataMining.load_model()
            result = DataMining.get_research_relation(solicitud_datamining['email'])
            if result:
                return Response(json.dumps(result), status=200, mimetype='application/json')
            else:
                return Response(status=204)
        except Exception as e:
            abort(400, description=str(e))  

class DataMiningGetResearchTag(Resource):
    def post(self):
        """
        Devuelve una lista de emails asociados a investigadores los cuales cumplen que tienen alguna relación con los tags dados como parámetros.
        """
        solicitud_datamining = request.get_json(force=True)
        try:
            result = {}
            DataMining.load_model()
            result = DataMining.get_research_tag(solicitud_datamining['tags'])
            if result:
                return Response(json.dumps(result), status=200, mimetype='application/json')
            else:
                return Response(status=204)
        except Exception as e:
            abort(400, description=str(e))  

class DataMiningGetResearchCategory(Resource):
    def post(self):
        """
        Devuelve una lista de emails asociados a los investigadores los cuales cumplen que tienen alguna relación con las categories dadas como parámetros.
        """
        solicitud_datamining = request.get_json(force=True)
        try:
            result = {}
            DataMining.load_model()
            result = DataMining.get_research_category(solicitud_datamining['categories'])
            if result:
                return Response(json.dumps(result), status=200, mimetype='application/json')
            else:
                return Response(status=204)
        except Exception as e:
            abort(400, description=str(e))  

class DataMiningGetResearchCategoryTag(Resource):
    def post(self):
        """
        Devuelve una lista de emails asociados a los investigadores lo cuales cumplen que tienen alguna relación con las categories y tags dados como parámetros.
        """
        solicitud_datamining = request.get_json(force=True)
        try:
            result = {}
            DataMining.load_model()
            result = DataMining.get_research_category_tag(solicitud_datamining['tags'], solicitud_datamining['categories'])
            if result:
                return Response(json.dumps(result), status=200, mimetype='application/json')
            else:
                return Response(status=204)
        except Exception as e:
            abort(400, description=str(e))  

api.add_resource(PDF2Table, '/api/module_cognitive/pdf_to_table/', endpoint='pdf_to_table_execute_resource')
api.add_resource(ExtractXMLExecute, '/api/module_cognitive/xml/execute', endpoint='xml_execute_resource')
api.add_resource(ExtractXMLGetDocument, '/api/module_cognitive/xml/get_document', endpoint='xml_get_document_resource')
api.add_resource(ExtractXMLGetDictionary, '/api/module_cognitive/xml/get_dictionary', endpoint='xml_get_dictionary_resource')
api.add_resource(WebScrappingBDNSSearch, '/api/module_cognitive/bdns/search', endpoint='bdns_search_date_resource')
api.add_resource(WebScrappingBDNSData, '/api/module_cognitive/bdns/data', endpoint='bdns_data_resource')
api.add_resource(DataMiningGetAllCluster, '/api/module_cognitive/datamining/all_cluster', endpoint='datamining_all_cluster_resource')
api.add_resource(DataMiningGetAllCategories, '/api/module_cognitive/datamining/all_categories', endpoint='datamining_all_categories_resource')
api.add_resource(DataMiningGetAllTag, '/api/module_cognitive/datamining/all_tag', endpoint='datamining_all_tag_resource')
api.add_resource(DataMiningGetCategoriesInterestResearch, '/api/module_cognitive/datamining/categories_interest_research', endpoint='datamining_categories_interest_research_resource')
api.add_resource(DataMiningGetTagsInterestResearch, '/api/module_cognitive/datamining/tags_interest_research', endpoint='datamining_tags_interest_research_resource')
api.add_resource(DataMiningGetResearchClusters, '/api/module_cognitive/datamining/research_clusters', endpoint='datamining_research_clusters_resource')
api.add_resource(DataMiningGetResearchRelation, '/api/module_cognitive/datamining/research_relation', endpoint='datamining_research_relation_resource')
api.add_resource(DataMiningGetResearchTag, '/api/module_cognitive/datamining/research_tag', endpoint='datamining_research_tag_resource')
api.add_resource(DataMiningGetResearchCategory, '/api/module_cognitive/datamining/research_category', endpoint='datamining_research_category_resource')
api.add_resource(DataMiningGetResearchCategoryTag, '/api/module_cognitive/datamining/research_category_tag', endpoint='datamining_research_category_tag_resource')
