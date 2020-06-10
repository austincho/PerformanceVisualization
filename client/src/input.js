import React, { Component } from 'react';
import FormControl from '@material-ui/core/FormControl';
import Button from '@material-ui/core/Button';
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
                }
            ]
        }
    }

    submit() {
        if (this.state.graphSelected !== 0 && this.state.functionSelected !== 0 && this.state.input !== '' && this.state.prediction !== '') {
            if (parseInt(this.state.prediction) <= 0 || parseInt(this.state.input) <= 0) {
                this.setState({showError: true, errorText: 'Please choose an Integer > 0'});
            } else {
                this.setState({showError: false, errorText: ''});
                this.submitForm();
            }
        } else {
            this.setState({showError: true, errorText: 'Please provide input for every box in the form.'});
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
        }).catch(e => {
            console.log('error: ', e);
            this.setState({showError: true, errorText: 'error'});
            console.log(this.state.errorText);
        });
    }

    createGraphs(data) {
        // TODO: parse (x,y) points for graphs from data parameter

        let traceData, layout;
        switch (this.state.graphSelected) {
            case "line":
                let trace = {
                    x:[1,2,3,4,5],
                    y:[1,2,3,4,15],
                    mode: 'lines',
                    name: 'Test'
                }
                traceData = [trace];
                layout = {
                    title: 'Line Chart'
                };
                break;

            case "bar":
                let bar = {
                    x:[1,2,3,4,5],
                    y:[1,2,3,4,5],
                    type: 'bar'
                }
                traceData = [bar];
                layout = {
                    title: 'Bar Report'
                }
                break;

            case "area":
                let area = {
                    x:[1,2,3,4,5],
                    y:[1,2,3,4,15],
                    mode: 'lines',
                    fill: 'tozeroy',
                    name: 'Test'
                }
                traceData = [area];
                layout = {
                    title: 'Memory Usage Area Chart'
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
                {this.state.data !== null && this.state.layout !== null &&
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