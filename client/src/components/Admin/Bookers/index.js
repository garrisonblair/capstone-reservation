import React, { Component } from 'react';
import {
  Table, Segment,
} from 'semantic-ui-react';
import './Bookers.scss';
import api from '../../../utils/api';
import BookerRow from './BookerRow';


class Bookers extends Component {
  state = {
    bookers: [],
    isLoading: false,
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

  render() {
    const { bookers, isLoading } = this.state;
    return (
      <div id="bookers">
        <h1>Bookers</h1>
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
        </Segment>
      </div>
    );
  }
}

export default Bookers;
