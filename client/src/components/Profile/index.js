/* eslint-disable prefer-const */
/* eslint-disable jsx-a11y/label-has-for */
import React, { Component } from 'react';
import PropTypes from 'prop-types';
import {
  Button,
  Form,
  Segment,
} from 'semantic-ui-react';
import sweetAlert from 'sweetalert2';
import Navigation from '../Navigation';
import api from '../../utils/api';
import storage from '../../utils/local-storage';
import AuthenticationRequired from '../HOC/AuthenticationRequired';
import getEmailRegex from '../../utils/emailRegex';
import './Profile.scss';


class Profile extends Component {
  state = {
    secondaryEmail: '',
    studentID: '',
    oldPassword: '',
    newPassword: '',
    confirmNewPassword: '',
  }

  componentDidMount() {
    api.getUser(storage.getUser().id)
      .then((response) => {
        let {
          booker_id: studentID,
          secondary_email: secondaryEmail,
        } = response.data.booker_profile;
        studentID = studentID === null ? '' : studentID;
        secondaryEmail = secondaryEmail === null ? '' : secondaryEmail;
        this.setState({ studentID, secondaryEmail });
      });
  }

  handleInputChange = (field, event) => {
    this.setState({ [field]: event.target.value });
  }

  updateProfile = () => {
    let { secondaryEmail, studentID } = this.state;
    const data = {
      booker_id: studentID,
      secondary_email: secondaryEmail,
    };

    let preventSubmit = false;
    const validEmail = secondaryEmail.match(getEmailRegex()) !== null;

    if (secondaryEmail === null || secondaryEmail === '' || secondaryEmail.length === 0) {
      delete data.secondary_email;
    }

    if (studentID === null || studentID === '' || studentID.length === 0) {
      delete data.booker_id;
    }

    if (studentID.length === 0 && secondaryEmail.length === 0) {
      preventSubmit = true;
    }

    if (studentID.length === 0 || secondaryEmail.length === 0) {
      preventSubmit = true;
      sweetAlert(
        ':(',
        'Please fill all the fields.',
        'error',
      );
      return;
    }

    if (secondaryEmail.length !== 0 && !validEmail) {
      preventSubmit = true;
      sweetAlert(
        ':(',
        'Please enter a valid email.',
        'error',
      );
      return;
    }

    if (studentID.length !== 8) {
      preventSubmit = true;
      sweetAlert(
        ':(',
        'ID should have 8 digits.',
        'error',
      );
      return;
    }

    if (!studentID.match('^[0-9]*$')) {
      preventSubmit = true;
      sweetAlert(
        ':(',
        'ID should have only digits.',
        'error',
      );
      return;
    }

    if (preventSubmit) {
      return;
    }

    api.updateUser(storage.getUser().id, data)
      .then(() => {
        sweetAlert(
          'Profile',
          'Profile saved successfully',
          'success',
        );
      })
      .catch(() => {
        sweetAlert(
          ':(',
          'There was an error.',
          'error',
        );
      });
  }

  updatePassword = () => {
    const { oldPassword, newPassword, confirmNewPassword } = this.state;
    let preventSubmit = false;

    if (oldPassword === null || oldPassword === '' || oldPassword.length === 0) {
      preventSubmit = true;
    }

    if (newPassword === null || newPassword === '' || newPassword.length === 0) {
      preventSubmit = true;
    }

    if (confirmNewPassword === null || confirmNewPassword === '' || confirmNewPassword.length === 0) {
      preventSubmit = true;
    }

    if (oldPassword.length === 0 || newPassword.length === 0 || confirmNewPassword.length === 0) {
      sweetAlert(
        ':(',
        'Please fill all the fields.',
        'error',
      );
    }

    if (newPassword !== confirmNewPassword) {
      preventSubmit = true;
      sweetAlert(
        ':(',
        'Password do not match.',
        'error',
      );
    }

    if (preventSubmit) {
      return;
    }

    const data = {
      old_password: oldPassword,
      new_password: newPassword,
    };

    api.updateUser(storage.getUser().id, data)
      .then(() => {
        sweetAlert(
          'Password Update',
          'Password updated successfully',
          'success',
        )
          .then(() => {
            this.setState({
              oldPassword: '',
              newPassword: '',
              confirmNewPassword: '',
            });
          });
      })
      .catch(() => {
        sweetAlert(
          ':(',
          'There was an error.',
          'error',
        );
      });
  }

  render() {
    const {
      secondaryEmail,
      studentID,
      oldPassword,
      newPassword,
      confirmNewPassword,
    } = this.state;

    const { asPage } = this.props;

    return (
      <div>
        { asPage ? <Navigation /> : null }
        <div className="profile">
          <Segment>
            <h1> Profile </h1>
            <Form>
              <Form.Field>
                <Form.Input
                  label="Secondary Email"
                  value={secondaryEmail}
                  onChange={(e) => { this.handleInputChange('secondaryEmail', e); }}
                />
              </Form.Field>
              <Form.Field>
                <Form.Input
                  label="Student ID"
                  type="number"
                  min="0"
                  value={studentID}
                  onChange={(e) => { this.handleInputChange('studentID', e); }}
                />
              </Form.Field>
              <Button primary onClick={this.updateProfile}> Update profile </Button>
            </Form>
          </Segment>
          <Segment>
            <h1> Update Password </h1>
            <Form>
              <Form.Field>
                <Form.Input
                  label="Old password"
                  type="password"
                  value={oldPassword}
                  onChange={(e) => { this.handleInputChange('oldPassword', e); }}
                />
              </Form.Field>
              <Form.Field>
                <Form.Input
                  label="New password"
                  type="password"
                  value={newPassword}
                  onChange={(e) => { this.handleInputChange('newPassword', e); }}
                />
              </Form.Field>
              <Form.Field>
                <Form.Input
                  label="Confirm new password"
                  type="password"
                  value={confirmNewPassword}
                  onChange={(e) => { this.handleInputChange('confirmNewPassword', e); }}
                />
              </Form.Field>
              <Button primary onClick={this.updatePassword}> Update password </Button>
            </Form>
          </Segment>
        </div>
      </div>
    );
  }
}

Profile.propTypes = {
  asPage: PropTypes.bool,
};

Profile.defaultProps = {
  asPage: false,
};


export default AuthenticationRequired(Profile);
