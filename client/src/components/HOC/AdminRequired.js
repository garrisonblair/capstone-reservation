import React, {Component} from 'react';
import api from '../../utils/api';


function AdminRequired(InnerComponent) {
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
        if (!data.is_superuser) {
          history.push('/');
        }
      })
      .catch((error) => {
        console.log(error);
      })
    }

    render() {
      return <InnerComponent {...this.props}/>
    }
  }

  return HOC;
}

export default AdminRequired;
