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
    api.getUsers()
      .then((r) => {
        if (r.status === 200) {
          console.log(r.data);
          this.setState({ bookers: r.data });
        }
      });
  }

  render() {
    const { bookers } = this.state;
    return (
      <div id="bookers">
        <Table>
          <Table.Header>
            <Table.Row key="-1">
              <Table.HeaderCell textAlign="center">
                User
              </Table.HeaderCell>
              <Table.HeaderCell>
                {}
              </Table.HeaderCell>
            </Table.Row>
          </Table.Header>
          <Table.Body>
            {bookers.map(b => (
              <BookerRow booker={b} key={b.id} />
            ))}
          </Table.Body>
        </Table>
      </div>
    );
  }
}

export default Bookers;
