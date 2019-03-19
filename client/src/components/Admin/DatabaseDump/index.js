/* eslint-disable no-console */
/* eslint-disable react/prefer-stateless-function */
import React, { Component } from 'react';
import { Button, Dropdown, Form, Header, Icon, Segment } from 'semantic-ui-react';
import api from '../../../utils/api';
import './DatabaseDump.scss';

class DatabaseDump extends Component {

  state = {
    models: [],
    selectedModel: '',
  }

  componentDidMount() {
    this.getModels();
  }

  getModels = () => {
    api.getCSV()
      .then((response) => {
        const { data: models } = response;
        this.setState({ models });
      });
  }

  onDropDownChange = (event, data) => {
    this.setState({ selectedModel: data.value });
  }

  renderDropDown = () => {
    const { models, selectedModel } = this.state;

    let modelOptions = [];
    modelOptions = models.map((model, index) => ({ key: index, value: model, text: model }));
    return (
      <Dropdown
        placeholder="Select Model"
        fluid
        search
        selection
        options={modelOptions}
        value={selectedModel}
        onChange={this.onDropDownChange}
      />
    );
  }

  download = () => {
    const { selectedModel } = this.state;
    console.log(selectedModel);
  }

  renderCSVForm = () => {
    return (
      <Segment>
        <Form>
          <Header as="h2">
            CSV
          </Header>
          <Form.Field>
            {this.renderDropDown()}
          </Form.Field>
          <Form.Field>
            <Button primary onClick={this.download}>
              <Icon name="download" />
              Download
            </Button>
          </Form.Field>
        </Form>
      </Segment>
    )
  }

  render() {
    return (
      <div className="database-dump">
        <Header as="h1">
          <Icon name="database" />
          Database Dump
        </Header>
        {this.renderCSVForm()}
      </div>
    )
  }
}

export default DatabaseDump;
