import React, { Component } from 'react';
import { Table, Message } from 'semantic-ui-react';
import api from '../../utils/api';
import './GroupInvitations.scss';
import InvitationRow from './InvitationRow';

class GroupInvitations extends Component {
  state = {
    invitations: [],
  }

  componentDidMount() {
    this.syncInvitations();
  }

  syncInvitations = () => {
    api.getGroupInvitations()
      .then((r) => {
        if (r.status === 200) {
          this.setState({ invitations: r.data });
        }
      });
  }

  renderTable = () => {
    const { invitations } = this.state;
    return (
      <Table>
        <Table.Header>
          <Table.Row>
            <Table.HeaderCell>Group</Table.HeaderCell>
            <Table.HeaderCell>Owner</Table.HeaderCell>
            <Table.HeaderCell />
          </Table.Row>
        </Table.Header>
        <Table.Body>
          {invitations.map(
            i => <InvitationRow invitation={i} syncMethod={this.syncInvitations} key={i.id} />,
          )}
        </Table.Body>
      </Table>
    );
  }

  renderEmptyMessage = () => (
    <Message>
      <Message.Header>No result</Message.Header>
      <p>You don&lsquo;t have group invitations.</p>
    </Message>
  )

  render() {
    const { invitations } = this.state;
    return (
      <div id="group-invitations">
        <h1>Invitations</h1>
        {invitations.length === 0 ? this.renderEmptyMessage() : this.renderTable()}
      </div>
    );
  }
}

export default GroupInvitations;
