import React, { Component } from 'react';
import { Button, Dropdown, Label } from 'semantic-ui-react';
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
  }

  componentDidMount() {
    api.getPrivileges()
      .then((r) => {
        if (r.status === 200) {
          console.log(r.data);
          const { options } = this.state;
          r.data.filter(p => p.is_default === false)
            .map(p => options.push({ value: p.id, text: p.name, key: p.id }));
          this.setState({ options });
        }
      });
  }

  handleRequestPrivilege = () => {
    const { dropdownValue } = this.state;
    if (dropdownValue.length === 0) {
      sweetAlert('Empty field', 'Please choose a privilege', 'warning');
      return;
    }
    api.requestPrivilege()
      .then((r) => {
        console.log(r);
      });
  }

  handlePrivilegeChange = (e, v) => {
    console.log(v);
  }

  changeToPending = () => {
    this.setState({
      labelColor: 'yellow',
      buttonText: 'Edit',
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
      options, dropdownValue, labelText, labelColor, buttonText,
    } = this.state;
    return (
      <div id="groups-request-privilege">
        <div>
          <h3>Privilege</h3>
          <Label color={labelColor}>{labelText}</Label>
        </div>
        <br />
        <Dropdown
          placeholder="Privileges"
          options={options}
          selection
          value={dropdownValue}
          onChange={this.handlePrivilegeChange}
        />
        <Button color="blue" onClick={this.buttonOnClick}>{buttonText}</Button>
      </div>
    );
  }
}

export default RequestPrivilege;
