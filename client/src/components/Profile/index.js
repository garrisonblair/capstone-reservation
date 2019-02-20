/* eslint-disable import/order */
/* eslint-disable no-unused-vars */
/* eslint-disable react/no-unused-state */
/* eslint-disable prefer-const */
/* eslint-disable no-console */
/* eslint-disable jsx-a11y/label-has-for */
/* eslint-disable react/prefer-stateless-function */
import React, { Component } from 'react';
import Navigation from '../Navigation';
import {
  Button,
  Form,
  // Icon,
  Segment,
} from 'semantic-ui-react';
// import api from '../../utils/api';
// import storage from '../../utils/local-storage';
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

  handleInputChange = (field, event) => {
    this.setState({ [field]: event.target.value });
  }

  updateProfile = () => {
    let { secondaryEmail, studentID } = this.state;
    console.log(secondaryEmail);
    console.log(studentID);
  }

  render() {
    return (
      <div>
        <Navigation />
        <div className="profile">
          <Segment>
            <h1> Profile </h1>
            <Form>
              <Form.Field>
                <Form.Input label="Secondary Email" onChange={(e) => { this.handleInputChange('secondaryEmail', e); }} />
              </Form.Field>
              <Form.Field>
                <Form.Input label="Student ID" onChange={(e) => { this.handleInputChange('studentID', e); }} />
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
