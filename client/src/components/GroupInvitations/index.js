import React, { Component } from 'react';
import {
  Table,
} from 'semantic-ui-react';
import api from '../../utils/api';
import './GroupInvitations.scss';

class GroupInvitations extends Component {
  state = {
    // invitations: []
  }

  componentDidMount() {
    this.syncInvitations();
  }

  syncInvitations = () => {
    api.getGroupInvitations()
      .then((r) => {
        console.log(r);
      });
  }

  render() {
    return (
      <div id="group-invitations">
        <Table>
          <Table.Header>
            <Table.Row>
              <Table.HeaderCell>Group</Table.HeaderCell>
              <Table.HeaderCell>Group owner</Table.HeaderCell>
            </Table.Row>
          </Table.Header>
        </Table>
      </div>
    );
  }
}

export default GroupInvitations;
