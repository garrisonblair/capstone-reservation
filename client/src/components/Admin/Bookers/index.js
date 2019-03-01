import React, { Component } from 'react';
import {
  Table, Segment, Pagination, Form, Button,
} from 'semantic-ui-react';
import './Bookers.scss';
import api from '../../../utils/api';
import BookerRow from './BookerRow';


class Bookers extends Component {
  state = {
    bookers: [],
    isLoading: false,
    activePage: 1,
    totalPages: 8,
    dropdownOptions: [
      { text: 'Any', value: 'Any' },
      { text: 'Yes', value: true },
      { text: 'No', value: false }],
    valueActive: 'Any',
    valueSuperUser: 'Any',
  }

  componentDidMount() {
    this.syncBookers();
  }

  syncBookers = () => {
    this.setState({ isLoading: true });
    api.getUsers()
      .then((r) => {
        this.setState({ isLoading: false });
        if (r.status === 200) {
          this.setState({ bookers: r.data });
        }
      });
  }

  handlePaginationChange = (e, data) => {
    console.log(data.activePage);
  }

  handleSearchOnChange = (e, data) => {
    console.log(data.value);
  }

  handleActiveOnChange = (e, { value }) => { this.setState({ valueActive: value }); }

  handleSuperUserOnChange = (e, { value }) => { this.setState({ valueSuperUser: value }); }

  render() {
    const {
      bookers, isLoading, activePage, totalPages, dropdownOptions, valueActive, valueSuperUser,
    } = this.state;
    return (
      <div id="bookers">
        <h1>Bookers</h1>
        <Form>
          <Form.Group widths="equal">
            <Form.Input fluid label="Search" icon="search" />
            <Form.Select fluid label="Super User" options={dropdownOptions} value={valueSuperUser} onChange={this.handleSuperUserOnChange} />
            <Form.Select fluid label="Active" options={dropdownOptions} value={valueActive} onChange={this.handleActiveOnChange} />
          </Form.Group>
          <Button>Search</Button>
        </Form>
        <Segment loading={isLoading}>
          <Table>
            <Table.Header>
              <Table.Row key="-1">
                <Table.HeaderCell textAlign="center">
                  Username
                </Table.HeaderCell>
                <Table.HeaderCell textAlign="center">
                  Full name
                </Table.HeaderCell>
                <Table.HeaderCell>
                  {}
                </Table.HeaderCell>
              </Table.Row>
            </Table.Header>
            <Table.Body>
              {bookers.map(b => (
                <BookerRow booker={b} key={b.id} syncBookers={this.syncBookers} />
              ))}
            </Table.Body>
          </Table>
          <Pagination
            defaultActivePage={activePage}
            totalPages={totalPages}
            onPageChange={this.handlePaginationChange}
          />
        </Segment>
      </div>
    );
  }
}

export default Bookers;
