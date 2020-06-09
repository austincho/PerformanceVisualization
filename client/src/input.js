import React, { Component } from 'react';
import FormControl from '@material-ui/core/FormControl';
import Button from '@material-ui/core/Button';
import InputLabel from '@material-ui/core/InputLabel';
import OutlinedInput from '@material-ui/core/OutlinedInput';
import TextField from '@material-ui/core/TextField';
import MenuItem from '@material-ui/core/MenuItem';

class Input extends Component {
    constructor(props) {
        super(props);
        this.state= {
            input: 0,
            prediction: 0,
            graphSelected: null,
            functionSelected: null,
            graphs:    [
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
                }]
        }
    }

    handleChange(){
        console.log('handlechange');
    }

    submit() {
        console.log('submit');
    }

    updateInput(key, value) {
        this.setState({
            [key]: value
        });
    }

    render() {
        return (
            <div>
                <div>
                    <FormControl variant="outlined">
                        <InputLabel htmlFor="command-input">Input value</InputLabel>
                        <OutlinedInput
                            id="input-value"
                            value={this.state.input}
                            onChange={e => this.updateInput("input", e.target.value)}
                            labelWidth={120}
                        />
                    </FormControl>
                </div>
                <div>
                    <FormControl variant="outlined">
                        <InputLabel htmlFor="command-input">Prediction input</InputLabel>
                        <OutlinedInput
                            id="prediction-input"
                            value={this.state.prediction}
                            onChange={e => this.updateInput("prediction", e.target.value)}
                            labelWidth={120}
                        />
                    </FormControl>
                </div>
                <div>
                    <TextField
                        id="select-graph"
                        select
                        label="Select Graph"
                        value={this.state.graphSelected}
                        onChange={this.handleChange()}
                        helperText="Please select your currency"
                    >
                        {this.state.graphs.map((option) => (
                            <MenuItem key={option.value} value={option.value}>
                                {option.label}
                            </MenuItem>
                        ))}
                    </TextField>
                </div>
                <div>
                    <Button size="large" variant="contained" color="primary" onClick={() => this.submit()}>
                        Enter
                    </Button>
                </div>
            </div>
        );
    }
}
export default Input;