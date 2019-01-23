import React, { Component } from 'react';
import { Table, Button } from 'semantic-ui-react';
import PropTypes from 'prop-types';
import sweetAlert from 'sweetalert2';
import api from '../../../utils/api';
import './PrivilegeRequestRow.scss';

class PrivilegeRequestRow extends Component {
  handleDeny = () => {
    const { request, syncMethod } = this.props;
    sweetAlert({
      title: 'Warning',
      html: `Are you sure you want to deny privilege to group ${request.group.name}? <br />Enter a reason.`,
      type: 'warning',
      input: 'text',
      showCancelButton: true,
      confirmButtonColor: '#3085d6',
      showLoaderOnConfirm: true,
      confirmButtonText: 'Deny',
      preConfirm: text => api.denyPrivilegeRequest(request.id, text)
        .then((r) => {
          if (r.status !== 200) {
            sweetAlert(':(', 'It did not approved.', 'error');
          }
        }),
      allowOutsideClick: () => !sweetAlert.isLoading(),
    }).then((r) => {
      if (r.value) {
        sweetAlert('Success', 'It denied successfully', 'success');
        syncMethod();
      }
    });
  }

  handleApprove = () => {
    const { request, syncMethod } = this.props;
    sweetAlert.fire({
      title: 'Confirmation',
      text: `Are you sure you want to approve privilege category '${request.privilege_category.name}'`
        + ` to group '${request.group.name}'?`,
      showCancelButton: true,
      confirmButtonText: 'Approve',
      showLoaderOnConfirm: true,
      preConfirm: () => api.approvePrivilegeRequest(request.id)
        .then((r) => {
          if (r.status !== 200) {
            sweetAlert(':(', 'It did not approved.', 'error');
          }
        })
        .catch(() => {
          sweetAlert(':(', 'It did not approved.', 'error');
        }),
      allowOutsideClick: () => !sweetAlert.isLoading(),
    }).then((result) => {
      if (result.value) {
        sweetAlert('Success', 'It approved successfully', 'success');
        syncMethod();
      }
    });
  }

  handleClickOnInfo = () => {
    const { request } = this.props;
    sweetAlert({
      title: 'Members',
      html: this.renderMembers(request.group.members),
      type: 'info',
    });
  }

  renderMembers = (members) => {
    const list = `<ul> ${members.map(m => `<li style="width:100px">${m.username}</li>`)}</ul>`;
    return list;
  }

  renderButtons = () => (
    <div>
      <Button color="blue" onClick={this.handleApprove}>Accept</Button>
      <Button color="red" onClick={this.handleDeny}>Deny</Button>
    </div>
  )

  render() {
    const { request } = this.props;
    return (
      <Table.Row className="privilege-request-row">
        <Table.Cell>
          {request.group.name}
          <Button circular icon="info circle" className="info-button" onClick={this.handleClickOnInfo} />
        </Table.Cell>
        <Table.Cell>
          {request.privilege_category.name}
        </Table.Cell>
        <Table.Cell>
          {request.status}
        </Table.Cell>
        <Table.Cell>
          {request.status === 'Pending' ? this.renderButtons() : null}
        </Table.Cell>
      </Table.Row>
    );
  }
}

PrivilegeRequestRow.propTypes = {
  // eslint-disable-next-line react/forbid-prop-types
  request: PropTypes.object.isRequired,
  syncMethod: PropTypes.func.isRequired,
};

export default PrivilegeRequestRow;
