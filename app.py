import tornado.ioloop
import tornado.web
from controllers.csv_reader import check_and_populate_control_table,populate_tables
from controllers.levantamento_controller import export_results_to_csv, get_highest_incidence_km

class ExportResultsHandler(tornado.web.RequestHandler):
    def get(self):
        highway = self.get_query_argument('highway', None)
        if highway is None:
            self.set_status(400)
            self.write({'error': 'Parâmetro highway é obrigatório.'})
            return

        success = export_results_to_csv(highway)
        if success:
            self.write({'message': f'Resultados da rodovia {highway} exportados para CSV com sucesso.'})
        else:
            self.set_status(500)
            self.write({'error': f'Falha ao exportar resultados da rodovia {highway} para CSV.'})

class HighestIncidenceKmHandler(tornado.web.RequestHandler):
    def get(self, item):
        highest_km = get_highest_incidence_km(item)
        if highest_km is not None:
            self.write({'highest_km': highest_km})
        else:
            self.set_status(404)
            self.write({'error': f"Não foi possível encontrar a Km com maior incidência do item '{item}'."})

class UpdateTablesHandler(tornado.web.RequestHandler):
    def post(self):
        check_and_populate_control_table()
        self.write({'message': 'Tabelas atualizadas com sucesso.'})

# Checar e popular a tabela controle antes de iniciar o servidor
check_and_populate_control_table()


# Iniciar o servidor
if __name__ == "__main__":
    app = tornado.web.Application([
        (r"/highest_incidence_km/([^/]+)", HighestIncidenceKmHandler),
        (r'/update_tables',UpdateTablesHandler),
        (r"/export_results", ExportResultsHandler),
    ])

    port = 8888
    app.listen(port)
    print(f"Servidor rodando na porta {port}")
    tornado.ioloop.IOLoop.current().start()