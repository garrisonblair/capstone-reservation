import React, { Component } from 'react';
import { Table, Message, Segment } from 'semantic-ui-react';
import PropTypes from 'prop-types';
import api from '../../utils/api';
import './GroupInvitations.scss';
import InvitationRow from './InvitationRow';

class GroupInvitations extends Component {
  state = {
    invitations: [],
    isLoading: false,
  }

  componentDidMount() {
    this.syncInvitations();
  }

  syncInvitations = () => {
    this.setState({ isLoading: true });
    api.getGroupInvitations()
      .then((r) => {
        this.setState({ isLoading: false });
        if (r.status === 200) {
          this.setState({ invitations: r.data });
        }
      });
  }

  renderTable = () => {
    const { invitations } = this.state;
    const { syncGroups } = this.props;
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
            i => (
              <InvitationRow
                invitation={i}
                syncGroups={syncGroups}
                syncMethod={this.syncInvitations}
                key={i.id}
              />
            ),
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
    const { invitations, isLoading } = this.state;
    return (
      <div id="group-invitations">
        <h1>Invitations</h1>
        <Segment loading={isLoading}>
          {invitations.length === 0 ? this.renderEmptyMessage() : this.renderTable()}
        </Segment>
      </div>
    );
  }
}

GroupInvitations.propTypes = {
  // eslint-disable-next-line react/forbid-prop-types
  syncGroups: PropTypes.func,
};

GroupInvitations.defaultProps = {
  syncGroups: null,
};

export default GroupInvitations;
