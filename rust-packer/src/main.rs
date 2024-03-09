use std::{
    fs::File,
    io::Read,
    env::args,
    process::exit
};
use libc::{mmap, munmap, MAP_ANONYMOUS, MAP_FAILED, MAP_PRIVATE, PROT_EXEC, PROT_READ};

fn main()
{
    let args = args().collect::<Vec<String>>();
    
    if args.len() != 2 {
        eprintln!("Usage : rust-packer <input_binary>");
        exit(1);
    }

    let buffer = load_binary_memory(args[1].clone()).ok().unwrap();
    //println!("{:?}", buffer);

    let addr = unsafe {
        mmap(std::ptr::null_mut(),
        buffer.len(),
        PROT_READ | PROT_EXEC,
        MAP_PRIVATE | MAP_ANONYMOUS,
        -1,
        0)
    };
    println!("{:?}", addr);

    if addr == MAP_FAILED {
        eprintln!("Failed to map memory");
        exit(1);
    }

    unsafe {
        std::ptr::copy_nonoverlapping(buffer.as_ptr(), addr as *mut u8, buffer.len());

        let func: extern "C" fn() = std::mem::transmute(addr);
        func();

        munmap(addr, buffer.len());
    }
    
}

fn load_binary_memory(path: String) -> std::io::Result<Vec<u8>>{
    let mut file = File::open(&path)?;
    let mut buffer = Vec::new();
    file.read_to_end(&mut buffer)?;
    Ok(buffer)
}