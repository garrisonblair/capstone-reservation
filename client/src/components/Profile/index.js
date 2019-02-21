/* eslint-disable no-unused-vars */
/* eslint-disable react/no-unused-state */
/* eslint-disable prefer-const */
/* eslint-disable no-console */
/* eslint-disable jsx-a11y/label-has-for */
/* eslint-disable react/prefer-stateless-function */
import React, { Component } from 'react';
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
    let preventSubmit = false;
    if (secondaryEmail === null || secondaryEmail === '' || secondaryEmail.length === 0) {
      preventSubmit = true;
    }

    if (studentID === null || studentID === '' || studentID.length === 0) {
      preventSubmit = true;
    }

    if (preventSubmit === true) {
      return;
    }

    const data = {
      booker_id: studentID,
      secondary_email: secondaryEmail,
    };

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

  render() {
    const { secondaryEmail, studentID } = this.state;
    return (
      <div>
        <Navigation />
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
                <Form.Input label="Old password" type="password" />
              </Form.Field>
              <Form.Field>
                <Form.Input label="New password" type="password" />
              </Form.Field>
              <Form.Field>
                <Form.Input label="Confirm new password" type="password" />
              </Form.Field>
              <Button primary> Update password </Button>
            </Form>
          </Segment>
        </div>
      </div>
    );
  }
}

export default AuthenticationRequired(Profile);
