import React, { Component } from 'react';
import { Table } from 'semantic-ui-react';
import './Bookers.scss';
import api from '../../../utils/api';
import BookerRow from './BookerRow';


class Bookers extends Component {
  state = {
    bookers: [],
  }

  componentDidMount() {
    this.syncBookers();
  }

  syncBookers = () => {
    api.getBookers()
      .then((r) => {
        if (r.status === 200) {
          this.setState({ bookers: r.data });
        }
      });
  }

  render() {
    const { bookers } = this.state;
    return (
      <div id="bookers">
        <h1>Bookers</h1>
        <Table>
          <Table.Header>
            <Table.Row key="-1">
              <Table.HeaderCell textAlign="center">
                Username
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
      </div>
    );
  }
}

export default Bookers;
