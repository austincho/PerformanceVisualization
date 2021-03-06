import React, { Component } from 'react';
import FormControl from '@material-ui/core/FormControl';
import Button from '@material-ui/core/Button';
import CircularProgress from '@material-ui/core/CircularProgress';
import InputLabel from '@material-ui/core/InputLabel';
import OutlinedInput from '@material-ui/core/OutlinedInput';
import TextField from '@material-ui/core/TextField';
import MenuItem from '@material-ui/core/MenuItem';
import Alert from '@material-ui/lab/Alert';
import Plot from 'react-plotly.js';

import './App.css';
import Grid from '@material-ui/core/Grid';

class Input extends Component {
    constructor(props) {
        super(props);
        this.state= {
            input: '',
            data: null,
            layout: null,
            prediction: '',
            graphSelected: 0,
            functionSelected: 0,
            errorText: '',
            showError: false,
            loading: false,
            graphs:    [
                {
                    value: 0,
                    label: 'Please select'
                },
                {
                    value: 'line',
                    label: 'Line',
                },
                {
                    value: 'bar',
                    label: 'Bar',
                },
                {
                    value: 'area',
                    label: 'Area',
                }],
            functions: [
                {
                    value: 0,
                    label: 'Please select'
                },
                {
                    value: 1,
                    label: 'Fibonacci(n)'
                },
                {
                    value: 2,
                    label: 'Square Root(n)'
                },
                {
                    value: 3,
                    label: 'Merge Sort n random integers'
                },
                {
                    value: 4,
                    label: 'Length of an array of size n'
                }
            ]
        }
    }

    submit() {
        this.setState({loading: true});
        if (this.state.graphSelected !== 0 && this.state.functionSelected !== 0 && this.state.input !== '' && this.state.prediction !== '') {
            if (parseInt(this.state.prediction) <= 0 || parseInt(this.state.input) <= 0) {
                this.setState({showError: true, errorText: 'Please choose an Integer > 0', loading: false});
            } else if (parseInt(this.state.prediction) <= parseInt(this.state.input)) {
                this.setState({showError: true, errorText: 'Please choose a prediction value > input value', loading: false});
            } else {
                this.setState({showError: false, errorText: ''});
                this.submitForm();
            }
        } else {
            this.setState({showError: true, errorText: 'Please provide input for every box in the form.', loading: false});
        }
    }

    submitForm() {
        const formInput = {
            inputValue: this.state.input,
            predictionValue: this.state.prediction,
            graphSelected: this.state.graphSelected,
            functionSelected: this.state.functionSelected
        };
        fetch('/submit', {
            method: 'post',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formInput)
        })
            .then(res => {
                console.log(res.status);
                if (res.status !== 200) {
                    this.setState({showError: true, errorText: res.json()});
                    return;
                }
                return res.json();
            }).then(output => {
            console.log(output);
            this.createGraphs(output.data);
            this.setState({loading: false});
        }).catch(e => {
            console.log('error: ', e);
            this.setState({showError: true, errorText: 'error', loading: false});
            console.log(this.state.errorText);
        });
    }

    createGraphs(data) {
        let xActual = [];
        let xPrediction = [];
        let yPrediction = [];
        let i = 1;
        while (i <= data["n"]) {
            xActual.push(i);
            if (i === data["n"]){
                xPrediction.push(i);
            }
            i++;
        }
        while(i <= data["m"]) {
            xPrediction.push(i);
            i++;
        }
        let yActual = data["actual"];
        data["prediction"].unshift(yActual.slice(-1)[0]);
        yPrediction = data["prediction"];

        let traceData, layout;
        switch (data["graphSelected"]) {
            case "line":
                let trace = {
                    x:xActual,
                    y:yActual,
                    mode: 'lines',
                    name: 'Actual'
                }
                let tracePred = {
                    x:xPrediction,
                    y:yPrediction,
                    mode:'dot',
                    name: 'Prediction'
                }
                traceData = [trace, tracePred];
                layout = {
                    title: 'Runtime Line Chart',
                    xaxis: {title: 'Input Size (n)'},
                    yaxis: {title: 'Runtime (ms)'}
                };
                break;

            case "bar":
                xPrediction.shift();
                yPrediction.shift();
                let bar = {
                    x:xActual,
                    y:yActual,
                    type: 'bar',
                    name: 'Actual'
                }
                let barPred = {
                    x:xPrediction,
                    y:yPrediction,
                    type: 'bar',
                    name: 'Prediction'
                }
                traceData = [bar, barPred];
                layout = {
                    title: 'RunTime Bar Chart',
                    xaxis: {title: 'Input Size (n)'},
                    yaxis: {title: 'Runtime (ms)'},
                }
                break;

            case "area":
                let area = {
                    x:xActual,
                    y:yActual,
                    mode: 'line',
                    fill: 'tozeroy',
                    name: 'Actual'
                }
                let areaPred = {
                    x:xPrediction,
                    y:yPrediction,
                    mode: 'line',
                    fill: 'tozeroy',
                    name: 'Prediction'
                }
                traceData = [area, areaPred];
                layout = {
                    title: 'Runtime Area Chart',
                    xaxis: {title: 'Input Size (n)'},
                    yaxis: {title: 'Runtime (ms)'}
                };
                break;
        }
        this.setState({data :traceData, layout: layout});
        console.log('creating graphs');
        console.log(data);
    }

    updateInput(key, value) {
        console.log('KEY: ', key);
        console.log('VALUE: ', value);
        this.setState({
            [key]: value
        });
    }

    render() {
        return (
            <div>
                <div>
                    <FormControl variant="outlined">
                        <InputLabel htmlFor="command-input">Input value n</InputLabel>
                        <OutlinedInput
                            id="input-value"
                            type="number"
                            value={this.state.input}
                            onChange={e => this.updateInput("input", e.target.value)}
                            labelWidth={120}
                        />
                    </FormControl>
                </div>
                <br></br>
                <div>
                    <FormControl variant="outlined">
                        <InputLabel htmlFor="command-input">Prediction input</InputLabel>
                        <OutlinedInput
                            id="prediction-input"
                            type="number"
                            value={this.state.prediction}
                            onChange={e => this.updateInput("prediction", e.target.value)}
                            labelWidth={120}
                        />
                    </FormControl>
                </div>
                <br></br>
                <div>
                    <TextField
                        id="select-graph"
                        select
                        label="Select Graph"
                        value={this.state.graphSelected}
                        onChange={e => this.updateInput("graphSelected", e.target.value)}
                        helperText="Please select a graph type"
                    >
                        {this.state.graphs.map((option) => (
                            <MenuItem key={option.value} value={option.value}>
                                {option.label}
                            </MenuItem>
                        ))}
                    </TextField>
                </div>
                <br></br>
                <div>
                    <TextField
                        id="select-function"
                        select
                        label="Select function"
                        value={this.state.functionSelected}
                        onChange={e => this.updateInput("functionSelected", e.target.value)}
                        helperText="Please select a function"
                    >
                        {this.state.functions.map((option) => (
                            <MenuItem key={option.value} value={option.value}>
                                {option.label}
                            </MenuItem>
                        ))}
                    </TextField>
                </div>
                <br></br>
                <div>
                    <Button size="large" variant="contained" color="primary" onClick={() => this.submit()}>Enter</Button>
                </div>
                <br></br>
                <div>
                    {this.state.showError &&
                    <Alert className="error" severity="error">{this.state.errorText}</Alert>
                    }
                </div>
                {this.state.loading === true && <div><CircularProgress /><span>loading...</span></div>}
                {this.state.data !== null && this.state.layout !== null && !this.state.loading && !this.state.showError &&
                <Plot
                    data={this.state.data}
                    layout={this.state.layout}
                    // frames={this.state.frames}
                    // config={this.state.config}
                    // onInitialized={(figure) => this.setState(figure)}
                    // onUpdate={(figure) => this.setState(figure)}
                />
                }
            </div>
        );
    }
}
export default Input;