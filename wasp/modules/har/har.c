// Include MicroPython API.
#include "py/runtime.h"
#include "py/obj.h"

// This is the function which will be called from Python as har.add_ints(a, b).
STATIC mp_obj_t har_add_ints(mp_obj_t a_obj, mp_obj_t b_obj) {
    // Extract the ints from the micropython input objects.
    int a = mp_obj_get_int(a_obj);
    int b = mp_obj_get_int(b_obj);

    // Calculate the addition and convert to MicroPython object.
    return mp_obj_new_int(a + b);
}

STATIC mp_obj_t har_add_ints_array(mp_obj_t list_x_obj, mp_obj_t list_y_obj, mp_obj_t list_z_obj) {
    // Extract the lists from the micropython input objects.
    mp_obj_list_t *list_x = MP_OBJ_TO_PTR(list_x_obj);
    mp_obj_list_t *list_y = MP_OBJ_TO_PTR(list_y_obj);
    mp_obj_list_t *list_z = MP_OBJ_TO_PTR(list_z_obj);

    // Ensure that all lists have the same length.
    size_t len = list_x->len;
    if (len != list_y->len || len != list_z->len) {
        nlr_raise(mp_obj_new_exception_msg_varg(&mp_type_ValueError,
            "Input lists must have the same length"));
    }

    // Initialize sums to 0.
    mp_int_t x_sum = 0;
    mp_int_t y_sum = 0;
    mp_int_t z_sum = 0;

    // Add corresponding elements of each list after converting to integers.
    for (size_t i = 0; i < len; i++) {
        mp_obj_t x_item = mp_obj_new_int_from_float(mp_obj_get_float(list_x->items[i]));
        mp_obj_t y_item = mp_obj_new_int_from_float(mp_obj_get_float(list_y->items[i]));
        mp_obj_t z_item = mp_obj_new_int_from_float(mp_obj_get_float(list_z->items[i]));

        // Add to sums.
        x_sum += MP_OBJ_SMALL_INT_VALUE(x_item);
        y_sum += MP_OBJ_SMALL_INT_VALUE(y_item);
        z_sum += MP_OBJ_SMALL_INT_VALUE(z_item);
    }

    // Create and return a tuple of the sums.
    mp_obj_tuple_t *result_tuple = MP_OBJ_TO_PTR(mp_obj_new_tuple(3, NULL));
    result_tuple->items[0] = MP_OBJ_NEW_SMALL_INT(x_sum);
    result_tuple->items[1] = MP_OBJ_NEW_SMALL_INT(y_sum);
    result_tuple->items[2] = MP_OBJ_NEW_SMALL_INT(z_sum);

    return MP_OBJ_FROM_PTR(result_tuple);
}

// Define a Python reference to the function above.
STATIC MP_DEFINE_CONST_FUN_OBJ_2(har_add_ints_obj, har_add_ints);
STATIC MP_DEFINE_CONST_FUN_OBJ_3(har_add_ints_array_obj, har_add_ints_array);

// Define all properties of the module.
// Table entries are key/value pairs of the attribute name (a string)
// and the MicroPython object reference.
// All identifiers and strings are written as MP_QSTR_xxx and will be
// optimized to word-sized integers by the build system (interned strings).
STATIC const mp_rom_map_elem_t har_module_globals_table[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_har) },
    { MP_ROM_QSTR(MP_QSTR_add_ints), MP_ROM_PTR(&har_add_ints_obj) },
    { MP_ROM_QSTR(MP_QSTR_add_ints_array), MP_ROM_PTR(&har_add_ints_array_obj) },
};
STATIC MP_DEFINE_CONST_DICT(har_module_globals, har_module_globals_table);

// Define module object.
const mp_obj_module_t har_user_cmodule = {
    .base = { &mp_type_module },
    .globals = (mp_obj_dict_t *)&har_module_globals,
};

// Register the module to make it available in Python.
// Note: the "1" in the third argument means this module is always enabled.
// This "1" can be optionally replaced with a macro like MODULE_HAR_ENABLED
// which can then be used to conditionally enable this module.
MP_REGISTER_MODULE(MP_QSTR_har, har_user_cmodule, 1);
