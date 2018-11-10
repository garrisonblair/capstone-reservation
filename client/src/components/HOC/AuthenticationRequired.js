import React, {Component} from 'react';
import api from '../../utils/api';


function AuthenticationRequired(InnerComponent) {
  class HOC extends Component {
    componentDidMount() {
      const {history} = this.props;

      if (!localStorage.CapstoneReservationUser) {
        history.push('/');
        return;
      }

      api.getMyUser()
      .then((response) => {
        let {data} = response;
        // console.log(data);
      })
      .catch((error) => {
        console.log(error);
        history.push('/');
      })
    }

    render() {
      return <InnerComponent {...this.props}/>
    }
  }

  return HOC;
}

export default AuthenticationRequired;
