from fbprophet import Prophet
from fbprophet.plot import add_changepoints_to_plot
from fbprophet.diagnostics import cross_validation
import pandas as pd
import matplotlib.pyplot as plt

class Modelo_prophet_semanal:
    
    def __init__(self, dados:pd.DataFrame, teste_periodo=30, **kwargs_model):
        
        self.treino = dados[:len(dados) - teste_periodo]
        self.teste = dados[len(dados) - teste_periodo:]
        self.modelo = Prophet(daily_seasonality=False, yearly_seasonality=False, **kwargs_model)
        self.modelo.fit(self.treino)
        self.previsao = self.modelo.predict(self.modelo.make_future_dataframe(periods=teste_periodo))
    
    def plota(self, xlabel='', ylabel='', teste=True, changepoint=False, ax=None, show=False, month_freq=3, kwargs_modeloplot={}, kwargs_testeplot={}, linestyle=''):
    
        if ax is None:
            fig, ax = plt.subplots(figsize=(20,10))
            ax_none = True
        
        plt.sca(ax)
        self.modelo.plot(self.previsao, xlabel=xlabel, ylabel=ylabel, ax=ax, **kwargs_modeloplot)
        plt.plot(self.teste['ds'], self.teste['y'], linestyle = linestyle, **kwargs_testeplot)
        
        if len(self.teste) > 0:
            plt.xticks(pd.date_range(min(self.treino['ds']), max(self.teste['ds']), freq=f'{month_freq}MS'),pd.date_range(min(self.treino['ds']), max(self.teste['ds']), freq=f'{month_freq}MS').strftime('%Y-%b'))
        else:
            plt.xticks(pd.date_range(min(self.treino['ds']), max(self.treino['ds']), freq=f'{month_freq}MS'),pd.date_range(min(self.treino['ds']), max(self.treino['ds']), freq=f'{month_freq}MS').strftime('%Y-%b'))
        
        if changepoint is True:
            change = add_changepoints_to_plot(ax, self.modelo, self.previsao)
    
        if show is True:
            plt.show()
            
        elif ax_none is True:
            return fig
    
    def cross_validation(self, initial='180 days', period='30 days', horizon = '30 days'):
        self.cross = cross_validation(self.modelo, initial=initial, period=period, horizon=horizon)