import React, { Component } from 'react';
import { Table, Button } from 'semantic-ui-react';
import BookerModal from './BookerModal';
import './Bookers.scss';
import api from '../../../utils/api';


class Bookers extends Component {
  state = {
    bookers: [],
    showModal: false,
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

  onClickEditButton = () => {
    this.setState({ showModal: true });
  }

  render() {
    const { bookers, showModal } = this.state;
    return (
      <div id="bookers">
        <Table>
          <Table.Header>
            <Table.Row>
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
              <Table.Row key={b.id}>
                <Table.Cell textAlign="center">
                  {b.username}
                </Table.Cell>
                <Table.Cell>
                  <Button icon="edit" className="edit-button" onClick={this.onClickEditButton} />
                </Table.Cell>
              </Table.Row>
            ))}
            <BookerModal
              show={showModal}
              booker={b}
            />
          </Table.Body>
        </Table>
      </div>
    );
  }
}

export default Bookers;
