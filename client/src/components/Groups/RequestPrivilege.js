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
    labelText: 'none',
    labelColor: 'grey',
    buttonText: 'Request Privilege',
    currentStatus: 'new',
    disableDropdown: false,
    groupId: null,
    groupPrivilege: null,
  }

  componentDidMount() {
    const { groupId, groupPrivilege, justForTesting } = this.props;
    // This is just for testing.
    if (justForTesting) {
      const { options } = this.state;
      options.push({ value: 1, text: 'option 1', key: 1 });
    }

    this.setState({ groupId, groupPrivilege });
    api.getPrivileges()
      .then((r) => {
        if (r.status === 200) {
          const { options } = this.state;
          r.data.filter(p => p.is_default === false)
            .map(p => options.push({ value: p.id, text: p.name, key: p.id }));
          this.setState({ options });
        } else {
          sweetAlert(`${r.status} error`, r.text, 'error');
        }
      })
      .catch((r) => {
        console.log(r);
        sweetAlert('Something went wrong', r.text, 'error');
      });
    if (groupPrivilege !== null) {
      this.setState({ dropdownValue: groupPrivilege.privilege_category });
      if (groupPrivilege.status === 'Pending') {
        this.changeToPending();
      } else if (groupPrivilege.status === 'Denied') {
        this.changeToDenied();
      } else if (groupPrivilege.status === 'Approved') {
        this.changeToApproved();
      }
    }
  }

  handleRequestPrivilege = () => {
    const { dropdownValue, groupId } = this.state;
    if (dropdownValue.length === 0) {
      sweetAlert('Empty field', 'Please choose a privilege', 'warning');
      return;
    }
    api.requestPrivilege(groupId, dropdownValue)
      .then((r) => {
        if (r.status === 201) {
          this.changeToPending();
          this.setState({ groupPrivilege: r.data });
        } else {
          sweetAlert(`${r.status} error`, r.text, 'error');
        }
      })
      .catch((r) => {
        console.log(r);
        sweetAlert('Something went wrong', r.text, 'error');
      });
  }

  handleCancelRequest = () => {
    const { groupPrivilege } = this.state;
    api.cancelPrivilegeRequest(groupPrivilege.id)
      .then((r) => {
        if (r.status === 200) {
          this.changeToRequest();
        } else {
          sweetAlert(`${r.status} error`, r.text, 'error');
        }
      })
      .catch((r) => {
        console.log(r);
        sweetAlert('Something went wrong', r.text, 'error');
      });
  }

  handlePrivilegeChange = (e, v) => {
    this.setState({ dropdownValue: v.value });
  }

  changeToRequest = () => {
    this.setState({
      labelColor: 'grey',
      buttonText: 'Request Privilege',
      labelText: 'none',
      disableDropdown: false,
      currentStatus: 'new',
    });
  }

  changeToPending = () => {
    this.setState({
      labelColor: 'yellow',
      buttonText: 'Cancel Request',
      labelText: 'pending',
      disableDropdown: true,
      currentStatus: 'pending',
    });
  }

  changeToApproved = () => {
    this.setState({
      labelColor: 'green',
      buttonText: '',
      labelText: 'approved',
      disableDropdown: true,
      currentStatus: 'approved',
    });
  }

  changeToDenied = () => {
    this.setState({
      labelColor: 'red',
      buttonText: 'Make new Request',
      labelText: 'denied',
      disableDropdown: true,
      currentStatus: 'denied',
    });
  }

  buttonOnClick = () => {
    const { currentStatus } = this.state;
    if (currentStatus === 'new') {
      this.handleRequestPrivilege();
    } else if (currentStatus === 'pending') {
      this.handleCancelRequest();
    } else if (currentStatus === 'denied') {
      this.changeToRequest();
    }
  }

  render() {
    const {
      options, labelText, labelColor, buttonText, disableDropdown, dropdownValue, currentStatus,
    } = this.state;
    // if there is no privilege show nothing.
    if (options.length === 0) {
      return ('');
    }
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
          value={dropdownValue}
        />
        {currentStatus !== 'approved' ? (
          <Button
            color="blue"
            onClick={this.buttonOnClick}
            className="button-right"
          >
            {buttonText}
          </Button>
        ) : null}
      </div>
    );
  }
}

RequestPrivilege.propTypes = {
  groupId: PropTypes.number.isRequired,
  // eslint-disable-next-line react/forbid-prop-types
  groupPrivilege: PropTypes.object,
  justForTesting: PropTypes.bool,
};

RequestPrivilege.defaultProps = {
  groupPrivilege: null,
  justForTesting: false,
};

export default RequestPrivilege;
