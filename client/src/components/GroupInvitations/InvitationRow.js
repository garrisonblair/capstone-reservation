import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { Table, Button } from 'semantic-ui-react';
import sweetAlert from 'sweetalert2';
import api from '../../utils/api';

class InvitationRow extends Component {
  handleAccept = () => {
    const { invitation, syncMethod } = this.props;
    api.acceptInvitation(invitation.id)
      .then((r) => {
        if (r.status === 200) {
          sweetAlert('Sucess', 'Invitation was accepted', 'success');
          syncMethod();
        }
      });
  }

  hanleDecline = () => {
    const { invitation, syncMethod } = this.props;
    api.rejectInvitation(invitation.id)
      .then((r) => {
        if (r.status === 200) {
          sweetAlert('Sucess', 'Invitation was rejected', 'success');
          syncMethod();
        }
      });
  }

  render() {
    const { invitation } = this.props;
    return (
      <Table.Row key={invitation.id}>
        <Table.Cell>
          {invitation.group.name}
        </Table.Cell>
        <Table.Cell>
          {invitation.group.owner}
        </Table.Cell>
        <Table.Cell>
          <Button color="blue" onClick={this.handleAccept}>Accept</Button>
          <Button color="red" onClick={this.hanleDecline}>Decline</Button>
        </Table.Cell>
      </Table.Row>
    );
  }
}

InvitationRow.propTypes = {
  // eslint-disable-next-line react/forbid-prop-types
  invitation: PropTypes.object.isRequired,
  syncMethod: PropTypes.func.isRequired,
};


export default InvitationRow;
