/* eslint-disable no-param-reassign */
import React, { Component } from 'react';
import {
  Table, Segment, Pagination, Form, Button, Dropdown, Message,
} from 'semantic-ui-react';
import './Bookers.scss';
import api from '../../../utils/api';
import BookerRow from './BookerRow';


class Bookers extends Component {
  state = {
    bookers: [],
    isLoading: false,
    activePage: 1,
    totalPages: 0,
    dropdownOptions: [
      { text: 'Any', value: 'Any' },
      { text: 'Yes', value: true },
      { text: 'No', value: false }],
    valueActive: 'Any',
    valueSuperUser: 'Any',
    valueStaff: 'Any',
    valueSearch: '',
    searchLimit: 5,
  }

  componentDidMount() {
    const {
      searchLimit, valueSearch, valueActive, valueSuperUser, valueStaff, activePage,
    } = this.state;
    this.syncBookers(valueSearch, searchLimit, ((activePage * searchLimit) - searchLimit), valueActive, valueSuperUser, valueStaff);
  }

  syncBookers = (valueSearch, searchLimit, activePage, isActive, isSuperUser, isStaff) => {
    if (isActive === 'Any') {
      isActive = undefined;
    }
    if (isSuperUser === 'Any') {
      isSuperUser = undefined;
    }
    if (isStaff === 'Any') {
      isStaff = undefined;
    }
    this.setState({ isLoading: true });
    api.getUsers(valueSearch, searchLimit, activePage, isActive, isSuperUser, isStaff)
      .then((r) => {
        this.setState({ isLoading: false });
        if (r.status === 200) {
          this.setState({
            bookers: r.data.results,
            totalPages: Math.ceil(r.data.count / searchLimit),
          });
        }
      });
  }

  handlePaginationChange = (e, { activePage }) => {
    const {
      searchLimit, valueSearch, valueActive, valueSuperUser, valueStaff,
    } = this.state;
    this.setState({ activePage });
    const offset = ((activePage * searchLimit) - searchLimit);
    this.syncBookers(valueSearch, searchLimit, offset, valueActive, valueSuperUser, valueStaff);
  }

  handleSearchOnChange = (e, { value }) => { this.setState({ valueSearch: value }); }

  handleActiveOnChange = (e, { value }) => { this.setState({ valueActive: value }); }

  handleSuperUserOnChange = (e, { value }) => { this.setState({ valueSuperUser: value }); }

  handleStaffOnChange = (e, { value }) => { this.setState({ valueStaff: value }); }

  handleLimitOnChange = (e, { value }) => { this.setState({ searchLimit: value }); }

  handleSearchOnClick = () => {
    const {
      searchLimit, valueSearch, valueActive, valueSuperUser, valueStaff,
    } = this.state;
    this.setState({ activePage: 1 });
    this.syncBookers(valueSearch, searchLimit, 0, valueActive, valueSuperUser, valueStaff);
  }

  handleResetOnClick = () => {
    this.setState({
      valueActive: 'Any',
      valueSearch: '',
      valueStaff: 'Any',
      valueSuperUser: 'Any',
    });
  }

  render() {
    const {
      bookers, isLoading, activePage, totalPages,
      dropdownOptions, valueActive, valueSuperUser,
      valueStaff, valueSearch, searchLimit,
    } = this.state;
    return (
      <div id="bookers">
        <h1>Bookers</h1>
        <Form>
          <Form.Group widths="equal">
            <Form.Input fluid label="Search" icon="search" onChange={this.handleSearchOnChange} value={valueSearch} />
            <Form.Select fluid label="Super User" options={dropdownOptions} value={valueSuperUser} onChange={this.handleSuperUserOnChange} />
            <Form.Select fluid label="Active" options={dropdownOptions} value={valueActive} onChange={this.handleActiveOnChange} />
            <Form.Select fluid label="Staff" options={dropdownOptions} value={valueStaff} onChange={this.handleStaffOnChange} />
          </Form.Group>
          Table maximum size:
          <Dropdown
            className="table-max-size"
            options={[
              { text: 5, value: 5 },
              { text: 10, value: 10 },
              { text: 20, value: 20 },
              { text: 40, value: 40 },
            ]}
            selection
            compact
            value={searchLimit}
            onChange={this.handleLimitOnChange}
          />
          <br />
          <br />
          <Button color="blue" onClick={this.handleSearchOnClick}>
            Search
          </Button>
          <Button onClick={this.handleResetOnClick}>
            Reset
          </Button>
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
                <Table.HeaderCell textAlign="center">
                  Email
                </Table.HeaderCell>
                <Table.HeaderCell textAlign="center">
                  Super User
                </Table.HeaderCell>
                <Table.HeaderCell textAlign="center">
                  Staff
                </Table.HeaderCell>
                <Table.HeaderCell textAlign="center">
                  Active
                </Table.HeaderCell>
                <Table.HeaderCell />
              </Table.Row>
            </Table.Header>
            <Table.Body>
              {bookers.map(b => (
                <BookerRow
                  booker={b}
                  key={b.id}
                  syncBookers={() => this.syncBookers(
                    valueSearch, searchLimit, activePage, valueActive, valueSuperUser, valueStaff,
                  )
                  }
                />
              ))}
            </Table.Body>
          </Table>
          {bookers.length === 0 ? (
            <Message>
              <Message.Header>Empty list</Message.Header>
              <p>
                No bookers correspond to the specifications.
              </p>
            </Message>
          ) : null}
          {totalPages !== 0 ? (
            <Pagination
              activePage={activePage}
              totalPages={totalPages}
              onPageChange={this.handlePaginationChange}
            />
          ) : null}
        </Segment>
      </div>
    );
  }
}

export default Bookers;
