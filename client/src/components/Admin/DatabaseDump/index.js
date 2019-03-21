import React, { Component } from 'react';
import {
  Button, Dropdown, Form, Header, Icon, Segment,
} from 'semantic-ui-react';
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
    api.postCSV(selectedModel)
      .then((response) => {
        const { data } = response;
        const filename = `${selectedModel.toLowerCase()}.csv`;
        const blob = new Blob([data]);
        if (window.navigator.msSaveOrOpenBlob) { // IE hack; see http://msdn.microsoft.com/en-us/library/ie/hh779016.aspx
          window.navigator.msSaveBlob(blob, filename);
        } else {
          const a = window.document.createElement('a');
          a.href = window.URL.createObjectURL(blob, { type: 'text/csv' });
          a.download = filename;
          document.body.appendChild(a);
          a.click(); // IE: "Access is denied"; see: https://connect.microsoft.com/IE/feedback/details/797361/ie-10-treats-blob-url-as-cross-origin-and-denies-access
          document.body.removeChild(a);
        }
      });
  }

  renderCSVForm = () => {
    const { selectedModel } = this.state;
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
            <Button primary onClick={this.download} disabled={!selectedModel}>
              <Icon name="download" />
              Download
            </Button>
          </Form.Field>
        </Form>
      </Segment>
    );
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
    );
  }
}

export default DatabaseDump;
