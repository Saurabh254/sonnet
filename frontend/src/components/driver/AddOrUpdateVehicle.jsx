import {
    Dialog,
    DialogBackdrop,
    DialogPanel,
    DialogTitle,
} from "@headlessui/react";
import { ExclamationTriangleIcon } from "@heroicons/react/24/outline";

const UpdateVehicleComponent = () => {


    return (
        <Dialog open={open} onClose={onDecline} className="relative z-10">
            <DialogBackdrop className="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" />
            <div className="fixed inset-0 z-10 w-screen overflow-y-auto">
                <div className="flex min-h-full items-end justify-center p-4 text-center sm:items-center sm:p-0">
                    <DialogPanel className="relative transform overflow-hidden rounded-lg bg-white text-left shadow-xl transition-all sm:my-8 sm:w-full sm:max-w-lg">
                        <div className="bg-white px-4 pb-4 pt-5 sm:p-6 sm:pb-4">
                            <div className="sm:flex sm:items-start">
                                <div className="mx-auto flex h-12 w-12 flex-shrink-0 items-center justify-center rounded-full bg-red-100 sm:mx-0 sm:h-10 sm:w-10">
                                    <ExclamationTriangleIcon
                                        aria-hidden="true"
                                        className="h-6 w-6 text-red-600"
                                    />
                                </div>
                                <div className="mt-3 text-center sm:ml-4 sm:mt-0 sm:text-left">
                                    <DialogTitle
                                        as="h3"
                                        className="text-base font-semibold leading-6 text-gray-900"
                                    >
                                        New Ride Request.
                                    </DialogTitle>
                                    <RideDetails
                                        pickupLocation={pickupLocation}
                                        dropoffLocation={dropoffLocation}
                                        distance={distance}
                                        estimatedTime={estimatedTime}
                                        fare={fare}
                                        passengerName={passengerName}
                                        passengerContact={passengerContact}
                                    />
                                </div>
                            </div>
                        </div>
                        <div className="bg-gray-50 px-4 py-3 sm:flex sm:flex-row-reverse sm:px-6">
                            <button onClick={onAccept} className="btn btn-green">
                                Accept
                            </button>
                            <button onClick={onDecline} className="btn btn-red">
                                Reject
                            </button>
                        </div>
                    </DialogPanel>
                </div>
            </div>
        </Dialog>
    );
};



const AddVehicleComponent = () => {


    return (
        <Dialog open={open} onClose={onDecline} className="relative z-10">
            <DialogBackdrop className="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" />
            <div className="fixed inset-0 z-10 w-screen overflow-y-auto">
                <div className="flex min-h-full items-end justify-center p-4 text-center sm:items-center sm:p-0">
                    <DialogPanel className="relative transform overflow-hidden rounded-lg bg-white text-left shadow-xl transition-all sm:my-8 sm:w-full sm:max-w-lg">
                        <div className="bg-white px-4 pb-4 pt-5 sm:p-6 sm:pb-4">
                            <div className="sm:flex sm:items-start">
                                <div className="mx-auto flex h-12 w-12 flex-shrink-0 items-center justify-center rounded-full bg-red-100 sm:mx-0 sm:h-10 sm:w-10">
                                    <ExclamationTriangleIcon
                                        aria-hidden="true"
                                        className="h-6 w-6 text-red-600"
                                    />
                                </div>
                                <div className="mt-3 text-center sm:ml-4 sm:mt-0 sm:text-left">
                                    <DialogTitle
                                        as="h3"
                                        className="text-base font-semibold leading-6 text-gray-900"
                                    >
                                        New Ride Request.
                                    </DialogTitle>
                                    <RideDetails
                                        pickupLocation={pickupLocation}
                                        dropoffLocation={dropoffLocation}
                                        distance={distance}
                                        estimatedTime={estimatedTime}
                                        fare={fare}
                                        passengerName={passengerName}
                                        passengerContact={passengerContact}
                                    />
                                </div>
                            </div>
                        </div>
                        <div className="bg-gray-50 px-4 py-3 sm:flex sm:flex-row-reverse sm:px-6">
                            <button onClick={onAccept} className="btn btn-green">
                                Accept
                            </button>
                            <button onClick={onDecline} className="btn btn-red">
                                Reject
                            </button>
                        </div>
                    </DialogPanel>
                </div>
            </div>
        </Dialog>
    );
};
