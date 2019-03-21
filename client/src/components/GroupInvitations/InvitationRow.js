import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { Table, Button } from 'semantic-ui-react';
import sweetAlert from 'sweetalert2';
import api from '../../utils/api';

class InvitationRow extends Component {
  state = {
    groupOwner: '',
  }

  componentDidMount() {
    const { invitation } = this.props;
    api.getUsers()
      .then((r) => {
        const o = r.data.find(u => u.id === invitation.group.owner);
        this.setState({ groupOwner: o.username });
      });
  }

  handleAccept = () => {
    const { invitation, syncMethod, syncGroups } = this.props;
    api.acceptInvitation(invitation.id)
      .then((r) => {
        if (r.status === 200) {
          sweetAlert('Sucess', 'Invitation was accepted', 'success');
          syncMethod();
          syncGroups();
        }
      })
      .catch((error) => {
        sweetAlert.fire({
          position: 'top',
          type: 'error',
          title: 'Cannot Accept Invitation',
          text: error.response.data,
        });
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
    const { groupOwner } = this.state;
    return (
      <Table.Row className="invitation_row" key={invitation.id}>
        <Table.Cell>
          {invitation.group.name}
        </Table.Cell>
        <Table.Cell>
          {groupOwner}
        </Table.Cell>
        <Table.Cell>
          <Button color="blue" className="invitation_button" onClick={this.handleAccept}>Accept</Button>
          <Button color="red" className="invitation_button" onClick={this.hanleDecline}>Decline</Button>
        </Table.Cell>
      </Table.Row>
    );
  }
}

InvitationRow.propTypes = {
  // eslint-disable-next-line react/forbid-prop-types
  invitation: PropTypes.object.isRequired,
  syncMethod: PropTypes.func.isRequired,
  syncGroups: PropTypes.func,
};

InvitationRow.defaultProps = {
  syncGroups: null,
};

export default InvitationRow;
