from flask import Flask, render_template, request,jsonify
import requests
import json
import pandas as pd
import os
import numpy as np
import plotly
import plotly.graph_objects as go
import plotly.express as px


app = Flask(__name__)

def name_id(name, total=False):
    target = os.path.join(app.static_folder, 'base_client.csv')
    base=pd.read_csv(target, index_col="SK_ID_CURR")
    try:
        ind=base[base['name']==name].index.to_list()[0]
    except:
        ind=0
        donnees_json={}
    finally:
        if total==False:
            del base
            return ind
        else:
            donnees_json=base.loc[base["name"]==name,:].iloc[:,:-1].squeeze().to_json()
            donnees=base.loc[base["name"]==name,:].iloc[:,:-1]
            del base
            return ind, donnees_json, donnees

def id_appli(ind):

    target = os.path.join(app.static_folder, 'application.csv')
    base = pd.read_csv(target)#, index_col="SK_ID_CURR")
    i=np.where(base['SK_ID_CURR']==ind)[0][0]
    appli = base.iloc[i,:].to_dict()
    del base
    return appli

def scoring(donnees, no_modif=True):
    if no_modif==True:
        url = "https://epoupi-api-scoring.herokuapp.com/v1/scoring/"
        target = os.path.join(app.static_folder, 'seuil.txt')
    else:
        url = "https://epoupi-api-scoring.herokuapp.com/v1/scoring_modif/"
        target = os.path.join(app.static_folder, 'seuil_pipeline.txt')
    try:
        score = requests.post(url, data=donnees)
        score=score.json()
    except:
        return 0, 0
    else:
        score2=score['score']
        fichier = open(target, "r")
        seuil = fichier.read()
        fichier.close()
        return score2, float(seuil)

def buttons_boxplot(var, data_graph, individu):
    shapes = []
    largeur = (data_graph.loc["max", var]-data_graph.loc["min", var])
    larg = data_graph.loc["75%_0", var]-data_graph.loc["25%_0", var]
    if (larg > largeur/10) or ((float(individu[var]) > data_graph.loc["75%_0", var]) or (float(individu[var]) < data_graph.loc["25%_0", var])):
        shapes.append(dict(type="rect", x0=data_graph.loc["min_0", var], y0=12,
                    x1=data_graph.loc["max_0", var], y1=17, fillcolor='palegreen', line_color='palegreen'))
        shapes.append(dict(type="rect", x0=data_graph.loc["min_1", var], y0=20,
                    x1=data_graph.loc["max_1", var], y1=25, fillcolor='bisque', line_color='bisque'))
        largeur = (data_graph.loc["max", var]-data_graph.loc["min", var])/500
        minX = data_graph.loc["min", var]
        maxX = data_graph.loc["max", var]
    else:
        largeur = (data_graph.loc["75%_0", var]-data_graph.loc["25%_0", var])/500
        minX = min(data_graph.loc["25%_0", var], data_graph.loc["25%_1", var])
        maxX = max(data_graph.loc["75%_0", var], data_graph.loc["75%_1", var])

    shapes.append(dict(type="rect", x0=data_graph.loc["25%_0", var], y0=12,
                x1=data_graph.loc["75%_0", var], y1=17, fillcolor='limegreen', line_color='limegreen'))
    shapes.append(dict(type="rect", x0=data_graph.loc["25%_1", var], y0=20,
                x1=data_graph.loc["75%_1", var], y1=25, fillcolor='darkorange', line_color='darkorange'))
    shapes.append(dict(type="rect", x0=data_graph.loc["50%_0", var], y0=12, x1=largeur +
                data_graph.loc["50%_0", var], y1=17, fillcolor='darkgreen', line_color='darkgreen'))
    shapes.append(dict(type="rect", x0=data_graph.loc["50%_1", var], y0=20, x1=largeur +
                data_graph.loc["50%_1", var], y1=25, fillcolor='brown', line_color='brown'))
    shapes.append(dict(type="rect", x0=float(individu[var]), y0=8, x1=largeur+float(
        individu[var]), y1=29, fillcolor='blue', line_color='blue'))
    return shapes, largeur, minX, maxX

def boxplot(individu):
    target = os.path.join(app.static_folder, 'data_boxplot.csv')
    data_graph=pd.read_csv(target,index_col="Unnamed: 0")
    target = os.path.join(app.static_folder, 'feature_importance.csv')
    filoc=pd.read_csv(target)
    filoc.sort_values('importance',ascending=False,inplace=True)
    filist=list(filoc.loc[:,'feature'])

    layout = go.Layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)', yaxis=dict(tickmode='array', tickvals=[15, 23], ticktext=['Remboursé', 'Défaut de remboursement']))

    shapes0, largeur0, minX0, maxX0=buttons_boxplot(filist[0], data_graph=data_graph,individu=individu)
    fig = go.Figure(layout=layout)

    buttons = []
    for col in filist[0:50]:
        shapes, largeur, minX, maxX=buttons_boxplot(col,data_graph=data_graph,individu=individu)
        buttons.append(dict(label=col,
                            method='update',
                            args=[{},{'shapes':shapes,
                                'xaxis.range': [minX-largeur*10, maxX]}]))

    fig.update_layout(width=600, 
                    height=250,
                    yaxis_range=[7, 29],
                    xaxis_range=[minX0-largeur0*10, maxX0],
                    shapes=shapes0,
                    updatemenus=[dict(type='dropdown',buttons=buttons,active=0, direction='down', x=0,xanchor='left', y=1.1,yanchor="bottom",showactive=True)])

    return json.dumps(fig,cls=plotly.utils.PlotlyJSONEncoder)

def feat_importance():
    target = os.path.join(app.static_folder, 'feature_importance.csv')
    fi=pd.read_csv(target)
    fi.sort_values('importance',ascending=True,inplace=True)
    nbr_feat=len(fi)
    nbr_lignes=[5,10,15,20,nbr_feat]
    fig=go.Figure(px.bar(fi,x='importance',y='feature', labels={'feature':"",'importance':""},title="Variables de décision selon leur importance", height=500, width=500))
    fig.update_traces(marker_color='#9f9f9f')
    fig.update_layout(yaxis={"range":[nbr_feat-20,nbr_feat]},
                      plot_bgcolor='white',
                      updatemenus=[dict(type="buttons",
                        direction="right",
                        active=3,
                        x=1,
                        y=1.1,
                        buttons=[{"label": f"{k} lignes",
                                    "method": "relayout",
                                    "args":[{'yaxis.range':[nbr_feat-k,nbr_feat]}]}for k in nbr_lignes])])#.update_traces(visible=True, selector=0)

    return json.dumps(fig,cls=plotly.utils.PlotlyJSONEncoder)


@app.route("/")
def arrivee():
    return render_template("connexion.html", message="")

@app.route("/donnees/", methods = ['POST'])
def submit():
    if request.method == "POST":
        name = request.form['username']
        if name=="":
            return render_template("connexion.html", message="* Vous avez oublié d'entrer un nom")
        ind, donnees, data = name_id(name, total=True)
        if ind==0:
            return render_template("connexion.html", message="* Nom inconnu")
        content = id_appli(ind)
        content= content
    return render_template("donnees.html",  n = name, i = ind, content=content, donnees=donnees)#,s=score,d=data_json)

@app.route("/score/", methods = ['POST'])
def score():
    if request.method=="POST":
        result=request.form
        name=result['name']
        ind, donnees_json, envoi=name_id(name, total=True)
        donnees=id_appli(ind)
        donnees_partielles=result.to_dict(flat=True)
        for cle in donnees_partielles.keys():
            donnees[cle]=donnees_partielles[cle]
        donnees.pop("name")
        donnees=json.dumps(donnees)

        score, seuil=scoring(donnees, no_modif=False)
        graph_metric="/static/graph_metric_pipeline.png"
        chart1 = feat_importance()
        chart2 = boxplot(envoi)
        if score < seuil:
            resultat = "accordé!"
        elif score >= seuil:
            resultat="refusé..."
        else:
            resultat="Veuillez contacter le service informatique"
    else:
        donnees='Veuillez réessayer plus tard.'
        ind="no_id"
        name="échec"
    return render_template("score.html",  n=name, i=ind, resultat=round(score,3), s=round(seuil,3), decision=resultat, donnees=donnees, graph_metric=graph_metric, chart2=chart2,chart1=chart1)

@app.route("/score_no_modif/", methods = ['POST'])
def score_no_modif():
    if request.method=="POST":
        result=request.form
        name=result['name']
        ind, donnees, envoi=name_id(name, total=True)
        if ind==0:
            return render_template("score.html",  n=name, i=ind, resultat=0, s=0, decision="Erreur interne : ind=0", donnees=result)
        score, seuil=scoring(donnees, no_modif=True)
        if seuil==0:
            return render_template("score.html",  n=name, i=ind, resultat=0, s=0, decision="Erreur API", donnees=donnees)
        if score < seuil:
            resultat = "accordé!"
        elif score >= seuil:
            resultat="refusé..."
        else:
            resultat="Veuillez vérifier le code"
    else:
        donnees='Veuillez réessayer plus tard.'
        ind="no_id"
        name="échec"
    chart1 = feat_importance()
    chart2 = boxplot(envoi)
    graph_metric="/static/graph_metric_model.png"
    return render_template("score.html",  n=name, i=ind, resultat=round(score,3), s=round(seuil,3), decision=resultat, graph_metric=graph_metric, chart1=chart1, chart2=chart2)


def test_name_id():
    assert name_id(name="Ellaria", total=False)== 213818


if __name__ == "__main__":
    app.run(debug=True)