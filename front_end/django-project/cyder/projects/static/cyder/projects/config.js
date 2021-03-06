'use strict';
import { View, FOREACH, IF, ESCHTML } from '../viewlib.js';
import CyderAPI from '../api.js';
import notifyRESTError from '../api-notify-error.js';

export class ProjectConfig extends View {
    constructor(projectId, el) {
        super(el, 'div');
        this.loadProject(projectId);
    }
    loadProject(projectId, force = false) {
        this._projectId = projectId;
        let prom = CyderAPI.Project.get(this._projectId, force);
        if(prom instanceof Promise) {
            prom.catch((error) => notifyRESTError(error));
            this._ready = prom.then(() => { this.render(); this._plot(); });
        }
        else {
            this._ready = Promise.resolve();
        }
        this.render();
    }
    _plot() {
        let project = CyderAPI.Project.get(this._projectId);

        let startDate = Date.parse(project.settings.start);
        let endDate = Date.parse(project.settings.end);
        let dates = [];
        for(let date = startDate; date < endDate; date+=project.settings.timestep*1000)
            dates.push(new Date(date));

        let pv = {x: dates, y: project.config.pv, mode: 'lines', name: 'PV'};
        let ev = {x: dates, y: project.config.ev, mode: 'lines', name: 'EV'};
        let load = {x: dates, y: project.config.load, mode: 'lines', name: 'Load'};

        let data = [pv, ev, load];
        let layout = {
            yaxis: {
                title: 'Active load(kW)'
            }
        };
        Plotly.newPlot(this._html.plot, data, layout);
    }
    get _template() {
        let project = CyderAPI.Project.get(this._projectId);
        return `
        <h1>Configuration</h1>
        ${ IF(project instanceof Promise, () =>
            `<br>
            Loading...`
        , () =>
            `<h4>Project: ${ESCHTML(project.name)}</h4>
            <br>
            <div data-name="plot" style="height:70vh;"></div>`
        )}
        `;
    }
}
