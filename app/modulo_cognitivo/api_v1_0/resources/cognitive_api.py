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

class ExtractXMLTraerDocumento(Resource):
    def post(self):
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

class ExtractXMLObtenerDiccionario(Resource):
    def post(self):
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

api.add_resource(PDF2Table, '/api/modulo_cognitivo/pdf_to_table/', endpoint='pdf_to_table_execute_resource')
api.add_resource(ExtractXMLExecute, '/api/modulo_cognitivo/xml/execute', endpoint='xml_execute_resource')
api.add_resource(ExtractXMLTraerDocumento, '/api/modulo_cognitivo/xml/traer_documento', endpoint='xml_traer_documento_resource')
api.add_resource(ExtractXMLObtenerDiccionario, '/api/modulo_cognitivo/xml/obtener_diccionario', endpoint='xml_obtener_diccionario_resource')
api.add_resource(WebScrappingBDNSSearch, '/api/modulo_cognitivo/bdns/search', endpoint='bdns_search_date_resource')
api.add_resource(WebScrappingBDNSData, '/api/modulo_cognitivo/bdns/data', endpoint='bdns_data_resource')
api.add_resource(DataMiningGetAllCluster, '/api/modulo_cognitivo/datamining/all_cluster', endpoint='datamining_all_cluster_resource')
api.add_resource(DataMiningGetAllCategories, '/api/modulo_cognitivo/datamining/all_categories', endpoint='datamining_all_categories_resource')
api.add_resource(DataMiningGetAllTag, '/api/modulo_cognitivo/datamining/all_tag', endpoint='datamining_all_tag_resource')
api.add_resource(DataMiningGetCategoriesInterestResearch, '/api/modulo_cognitivo/datamining/categories_interest_research', endpoint='datamining_categories_interest_research_resource')
api.add_resource(DataMiningGetTagsInterestResearch, '/api/modulo_cognitivo/datamining/tags_interest_research', endpoint='datamining_tags_interest_research_resource')
api.add_resource(DataMiningGetResearchClusters, '/api/modulo_cognitivo/datamining/research_clusters', endpoint='datamining_research_clusters_resource')
api.add_resource(DataMiningGetResearchRelation, '/api/modulo_cognitivo/datamining/research_relation', endpoint='datamining_research_relation_resource')
api.add_resource(DataMiningGetResearchTag, '/api/modulo_cognitivo/datamining/research_tag', endpoint='datamining_research_tag_resource')
api.add_resource(DataMiningGetResearchCategory, '/api/modulo_cognitivo/datamining/research_category', endpoint='datamining_research_category_resource')
api.add_resource(DataMiningGetResearchCategoryTag, '/api/modulo_cognitivo/datamining/research_category_tag', endpoint='datamining_research_category_tag_resource')