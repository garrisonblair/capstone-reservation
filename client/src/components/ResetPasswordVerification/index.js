/* eslint-disable react/prop-types,no-bitwise */
import React, { Component } from 'react';
import { Redirect } from 'react-router';
import PropTypes from 'prop-types';
import {
  Loader, Form, Button, Icon, Step,
} from 'semantic-ui-react';
import sweetAlert from 'sweetalert2';
import api from '../../utils/api';
import CustomFormInput from './CustomFormInput';
import './Verification.scss';


class ResetPasswordVerification extends Component {
  state = {
    password: '',
    confirmPassword: '',
    errorMessagePassword: '',
    errorMessageConfirmPassword: '',
    isLoading: true,
    firstName: '',
    userId: 0,
  }

  componentDidMount() {
    // This props value is for testing.
    const { showFormForTesting, match } = this.props;
    const { token } = match.params;

    if (showFormForTesting) {
      this.setState({ isLoading: false });
    }

    if (token) {
      api.verify(token)
      .then((response) => {
        if (response.status === 200) {
          this.setState({
            isLoading: false,
            firstName: response.data.first_name,
            userId: response.data.id,
          });
          localStorage.setItem('CapstoneReservationUser', JSON.stringify(response.data));
        }
      })
      .catch((error) => {
        this.setState({ 
          showLoader: false,
          hasError: true 
        });
        if (error.message.includes('400')) {
          sweetAlert(
            'Verification link does not exist',
            "Link is expired.",
            'error',
          );
        }
        else {
          sweetAlert(
            ':(',
            'Unknown error',
            'error',
          );
        }
      });
    }
  }

  verifyPasswords = () => {
    const { password, confirmPassword } = this.state;
    let preventSubmit = false;
    let errorMessagePassword = '';
    let errorMessageConfirmPassword = '';

    if (password.length === 0) {
      preventSubmit = true;
      errorMessagePassword = 'Please enter a password';
    }

    if (confirmPassword.length === 0) {
      preventSubmit = true;
      errorMessageConfirmPassword = 'Please re-enter the password';
    }

    if (password !== confirmPassword) {
      preventSubmit = true;
      errorMessagePassword = 'Passwords do not match';
      errorMessageConfirmPassword = 'Passwords do not match';
    }

    this.setState({
      errorMessagePassword,
      errorMessageConfirmPassword,
    });

    return preventSubmit;
  }

  handleChangePassword = (event) => {
    this.setState({
      password: event.target.value,
      errorMessagePassword: '',
    });
  }

  handleChangeConfirmPassword = (event) => {
    this.setState({
      confirmPassword: event.target.value,
      errorMessageConfirmPassword: '',
    });
  }

  handleSubmit = () => {
    // Verify form before continuing transaction.
    const {
      userId, password,
    } = this.state;
    const { history } = this.props;

    const preventSubmit = this.verifyPasswords();

    if (preventSubmit) {
      return;
    }

    const data = {
      password,
    };
    console.log('boom');
    api.updateUser(userId, data)
      .then(() => {
        console.log('testing');
        sweetAlert(
          'Reset Password',
          'Password reset successfully',
          'success',
        )
          .then(() => {
            history.push('/');
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

  renderLoader = () => (
    <div>
      <Loader active inline="centered" size="large" />
    </div>
  )

  renderMainForm() {
    const {
      errorMessagePassword,
      errorMessageConfirmPassword,
      firstName,
    } = this.state;
    return (
      <div>
        <h1>Reset Password</h1>
        <Step.Group size="mini" widths={2}>
          <Step completed>
            <Icon name="envelope" />
            <Step.Content>
              <Step.Title>Step 1</Step.Title>
              <Step.Description>Username confirmation</Step.Description>
            </Step.Content>
          </Step>
          <Step active>
            <Icon name="cog" />
            <Step.Content>
              <Step.Title>Step 2</Step.Title>
              <Step.Description>Reset Password</Step.Description>
            </Step.Content>
          </Step>
        </Step.Group>

        <h2>
          Welcome
          {firstName}
        </h2>
        <Form>
          <CustomFormInput
            fluid
            size="medium"
            icon="key"
            type="password"
            iconPosition="left"
            title="Enter Password:"
            onChange={this.handleChangePassword}
            errormessage={errorMessagePassword}
          />

          <CustomFormInput
            fluid
            size="medium"
            icon="key"
            type="password"
            iconPosition="left"
            title="Confirm Password:"
            onChange={this.handleChangeConfirmPassword}
            errormessage={errorMessageConfirmPassword}
          />
        </Form>
        <Form.Field>
          <br />
          <Button fluid size="small" icon onClick={this.handleSubmit}>
            Save
          </Button>
        </Form.Field>
      </div>
    );
  }

  render() {
    const { isLoading } = this.state;
    if (this.state.hasError) {
      return <Redirect to='/' />;
    }
    return (
      <div id="resetPasswordVerification">
        <div className="container">
          {isLoading ? this.renderLoader() : this.renderMainForm()}
        </div>
      </div>
    );
  }
}

ResetPasswordVerification.propTypes = {
  showFormForTesting: PropTypes.bool,
};

ResetPasswordVerification.defaultProps = {
  showFormForTesting: false,
};

export default ResetPasswordVerification;
