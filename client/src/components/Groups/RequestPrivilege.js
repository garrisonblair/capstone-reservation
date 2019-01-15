import React, { Component } from 'react';
import { Button, Dropdown, Label } from 'semantic-ui-react';
import PropTypes from 'prop-types';
import sweetAlert from 'sweetalert2';
import api from '../../utils/api';
import './RequestPrivilege.scss';

class RequestPrivilege extends Component {
  state = {
    options: [],
    dropdownValue: '',
    labelText: 'optional',
    labelColor: 'grey',
    buttonText: 'Request Privilege',
    currentStatus: 'new',
    disableDropdown: false,
  }

  componentDidMount() {
    api.getPrivileges()
      .then((r) => {
        if (r.status === 200) {
          const { options } = this.state;
          r.data.filter(p => p.is_default === false)
            .map(p => options.push({ value: p.id, text: p.name, key: p.id }));
          this.setState({ options });
        }
      });
  }

  handleRequestPrivilege = () => {
    const { dropdownValue } = this.state;
    const { groupId } = this.props;
    if (dropdownValue.length === 0) {
      sweetAlert('Empty field', 'Please choose a privilege', 'warning');
      return;
    }
    api.requestPrivilege(groupId, dropdownValue)
      .then((r) => {
        if (r.status === 201) {
          this.changeToPending();
        }
      });
  }

  handlePrivilegeChange = (e, v) => {
    this.setState({ dropdownValue: v.value });
  }

  changeToPending = () => {
    this.setState({
      labelColor: 'yellow',
      buttonText: 'Edit',
      labelText: 'pending',
      disableDropdown: true,
    });
  }

  changeToDenied = () => {

  }

  buttonOnClick = () => {
    const { currentStatus } = this.state;
    if (currentStatus === 'new') {
      this.handleRequestPrivilege();
    }
  }

  render() {
    const {
      options, labelText, labelColor, buttonText, disableDropdown,
    } = this.state;
    return (
      <div id="groups-request-privilege">
        <div>
          <h3>Privilege</h3>
          <Label color={labelColor}>{labelText}</Label>
        </div>
        <br />
        <Dropdown
          disabled={disableDropdown}
          placeholder="Privileges"
          options={options}
          selection
          onChange={this.handlePrivilegeChange}
        />
        <Button color="blue" onClick={this.buttonOnClick}>{buttonText}</Button>
      </div>
    );
  }
}

RequestPrivilege.propTypes = {
  groupId: PropTypes.number.isRequired,
};

export default RequestPrivilege;
